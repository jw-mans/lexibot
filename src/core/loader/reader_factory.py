from typing import Type
import os
from .types import (
    Reader,
    PDFReader,
    MDReader,
    DocReader,
    RTFReader,
)

READERS: dict[str, Type[Reader]] = {
    ".pdf": PDFReader,
    ".txt": MDReader,
    ".md": MDReader,
    ".doc": DocReader,
    ".docx": DocReader,
    ".rtf": RTFReader,
}


def makeReader(file_path: str) -> Reader:
    ext = os.path.splitext(file_path)[1].lower()
    reader_cls = READERS.get(ext)
    if not reader_cls:
        raise ValueError(f"Unsupported file format: {ext}")
    return reader_cls()