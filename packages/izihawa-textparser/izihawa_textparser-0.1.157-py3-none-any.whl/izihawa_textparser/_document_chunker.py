import dataclasses
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from typing import Callable, List

from izihawa_textparser.utils import is_banned_section
from izihawa_textutils.utils import remove_markdown
from langchain_core.documents import Document
from unstructured.cleaners.core import clean, clean_extra_whitespace

from ._text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    text: str
    start_index: int
    length: int
    updated_at: int
    issued_at: int | None = None
    type: str | None = None
    language: str | None = None
    issns: list[str] | None = None
    table_name: str | None = None

    def get_unique_id(self):
        return f'{self.document_id}@{self.field}@{self.chunk_id}'


@dataclass
class StoredChunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    start_index: int
    length: int
    updated_at: int
    text: str | None = None
    issued_at: int | None = None
    type: str | None = None
    language: str | None = None
    issns: list[str] | None = None
    table_name: str | None = None

    def get_unique_id(self):
        return f'{self.document_id}@{self.field}@{self.chunk_id}'


def extract_title_parts(document: dict, split):
    title_parts = []
    if "title" in document:
        title_parts.append(document["title"])
    for hn in range(1, 7):
        if hn_value := split.metadata.get(f"h{hn}"):
            title_parts.append(hn_value)
    return title_parts


def _length_function(remove_tables: bool, text: str):
    cleaned_chunk = remove_markdown(text, remove_tables=remove_tables, escape_brackets=False)
    return len(cleaned_chunk)


def merge_chunks(a: Chunk, b: Chunk) -> Chunk:
    if a.chunk_id > b.chunk_id:
        t = a
        a = b
        b = t
    new_chunk = Chunk(**dataclasses.asdict(a))
    new_chunk.length = b.start_index - a.start_index + b.length
    new_chunk.text = a.text + "\n\n" + b.text
    return new_chunk


@dataclass
class TableParsingState:
    maybe_prefix_title: str | None = None
    prefix_string: str | None = None
    maybe_suffix_title: str | None = None
    suffix_string: str | None = None
    header: str | None = None
    collected_chunks: list[Chunk] = dataclasses.field(default_factory=list)

    def reset(self) -> None:
        name = self.most_probable_name()
        for collected_chunk in self.collected_chunks:
            collected_chunk.table_name = name

        self.maybe_prefix_title = None
        self.prefix_string = None
        self.maybe_suffix_title = None
        self.suffix_string = None
        self.header = None
        self.collected_chunks = []

    def most_probable_name(self) -> str | None:
        if self.maybe_prefix_title:
            return self.maybe_prefix_title
        if self.maybe_suffix_title:
            return self.maybe_suffix_title
        if self.prefix_string:
            return self.prefix_string
        if self.suffix_string:
            return self.suffix_string

    def accept(self, chunk: Chunk) -> None:
        all_parts = list(re.finditer(TABLE_RE, chunk.text))
        for match in all_parts:
            if suffix := match.group('suffix'):
                if not self.maybe_prefix_title and not self.prefix_string:
                    if submatch := re.search(r'[Tt]ab(?:\.|le)\s*(.+)', suffix):
                        self.maybe_suffix_title = submatch.group(1).strip()
                    else:
                        self.suffix_string = suffix.strip()
                    chunk.text = chunk.text.replace(
                        self.maybe_suffix_title or self.suffix_string,
                        '',
                        1
                    )
                self.collected_chunks.append(chunk)
                self.reset()
                continue

            if not match.group('prefix') and not match.group('suffix'):
                self.collected_chunks.append(chunk)

            if prefix := match.group('prefix'):
                if submatch := re.search(r'[Tt]ab(?:\.|le)\s+(.+)', prefix):
                    self.maybe_prefix_title = submatch.group(1).strip()
                else:
                    self.prefix_string = prefix.strip()
                chunk.text = chunk.text.replace(
                    self.maybe_prefix_title or self.prefix_string,
                    '',
                    1
                )

            self.collected_chunks.append(chunk)
        if not all_parts:
            self.reset()


TABLE_RE = re.compile(r'(?P<prefix>[^\n|]+\n{1,2})?(?P<table>(?:\|[^\n]+\|(?:\n|$))+)(?P<suffix>[^\n|]+)?', flags=re.DOTALL | re.MULTILINE)


def _get_language(document: dict):
    return document["languages"][0] if "languages" in document else None


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        max_extra_length: int = 60,
        chunk_overlap: int = 32,
        min_chunk_length: int = 32,
        add_metadata: bool = False,
        add_year: bool = False,
        return_each_line: bool = False,
        remove_tables: bool = False,
        strip_whitespace: bool = False,
        separators: list[str] | None = None,
        length_function: Callable[[str], int] | None = None
    ):
        if separators is None:
            separators = ["\n\n", "\n", " ", ""]
        if length_function is None:
            length_function = partial(_length_function, remove_tables)
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            keep_separator=True,
            strip_whitespace=strip_whitespace,
            length_function=length_function,
            separators=separators,
        )
        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
                ("####", "h4"),
                ("#####", "h5"),
                ("######", "h6"),
            ],
            return_each_line=return_each_line,
        )
        self._chunk_size = chunk_size
        self._max_extra_length = max_extra_length
        self._chunk_overlap = chunk_overlap
        self._min_chunk_length = min_chunk_length
        self._add_metadata = add_metadata
        self._add_year = add_year
        self._remove_tables = remove_tables
        self._length_function = length_function

    def _is_figure_header(self, text: str, min_chunk_length: int | None = None):
        if min_chunk_length is None:
            min_chunk_length = self._min_chunk_length
        return bool(re.search(r"^[Tt]ab(le|\.)", text)) or self._length_function(text) < min_chunk_length

    def _splits_to_chunks(self, document: dict, field: str, splits):
        chunks = []
        for chunk_id, split in enumerate(splits):
            page_content = str(split.page_content)
            chunk_text = clean(
                remove_markdown(
                    page_content,
                    remove_tables=self._remove_tables,
                    escape_brackets=False,
                ),
                extra_whitespace=False,
                dashes=True,
                bullets=True,
                trailing_punctuation=True,
            )
            chunk_text = re.sub('\n{2,}', '\n\n', chunk_text)
            title_parts = extract_title_parts(document, split)

            chunk = Chunk(
                document_id=document["id"],
                field=field,
                chunk_id=chunk_id,
                start_index=split.metadata["start_index"],
                length=len(page_content),
                issued_at=document.get("issued_at"),
                updated_at=document["updated_at"],
                type=document.get("type"),
                language=_get_language(document),
                title="\n".join(title_parts),
                text=chunk_text,
                issns=document.get("metadata", {}).get("issns"),
            )

            if any(is_banned_section(title_part) for title_part in title_parts):
                continue

            chunks.append(chunk)

        table_parsing = TableParsingState()
        for i, chunk in enumerate(chunks):
            table_parsing.accept(chunk)
        table_parsing.reset()

        enriched_chunks = []
        for chunk in chunks:
            chunk.text = clean_extra_whitespace(chunk.text).strip()
            chunk_length = self._length_function(chunk.text)
            if chunk_length > self._chunk_size:
                logging.warning(
                    f"Excessive chunk size: ({chunk_length}){chunk.text}"
                )
            if not chunk.text or chunk_length < self._min_chunk_length:
                continue
            if self._add_metadata:
                metadata = []
                if chunk.table_name:
                    metadata.append(f'TABLE: {chunk.table_name}')
                if chunk.title:
                    spaced_title = " ".join(chunk.title.split("\n"))
                    metadata.append(f'TITLE: {spaced_title}')
                metadata_str = '\n'.join(metadata)
                metadata_length = self._length_function(metadata_str)
                if metadata_str:
                    chunk.text += f'\n{metadata_str}'
                if chunk_length + metadata_length > self._chunk_size + self._max_extra_length:
                    logging.warning(
                        f"Excessive total length: ({chunk_length + metadata_length}){metadata}"
                    )
            if (
                self._add_year
                and "issued_at" in document
                and document.get("issued_at", -62135596800) != -62135596800
            ):
                issued_at = datetime.fromtimestamp(document["issued_at"], tz=None)
                chunk.text += f"\nYEAR: {issued_at.year}"
            enriched_chunks.append(chunk)
        return enriched_chunks

    def markdown_to_splits(self, text: str) -> list[Document]:
        return self._markdown_splitter.split_text(text)

    def text_to_splits(self, text: str) -> list[Document]:
        return self._text_splitter.split_documents(self.markdown_to_splits(text))

    def text_to_chunks(self, document, field):
        return self._splits_to_chunks(
            document,
            field,
            self.text_to_splits(document.get(field, "")),
        )

    def document_to_chunks(self, document: dict) -> List[Chunk]:
        return [
            *self.text_to_chunks(document, "abstract"),
            *self.text_to_chunks(document, "content"),
        ]

    def splits_to_text(self, splits) -> list[str]:
        previous_header = {}
        text_parts = []
        for split in splits:
            text = ""
            current_header = split.metadata
            for i in range(1, 7):
                h = f"h{i}"
                if previous_header.get(h) == current_header.get(h):
                    continue
                else:
                    for j in range(i, 7):
                        hj = f"h{j}"
                        if hj in current_header:
                            text_parts.append("#" * j + " " + current_header[hj])
                        else:
                            break
                    break
            text += split.page_content
            text_parts.append(text)
            previous_header = current_header
        return text_parts
