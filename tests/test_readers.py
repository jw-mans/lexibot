import pytest
from src.core.loader.reader_factory import makeReader, READERS

@pytest.mark.parametrize("file_name, expected_class_name", [
    ("document.pdf", "PDFReader"),
    ("notes.txt", "MDReader"),
    ("readme.md", "MDReader"),
    ("report.doc", "DocReader"),
    ("letter.docx", "DocReader"),
    ("file.rtf", "RTFReader"),
])
def test_makeReader_returns_correct_class(file_name, expected_class_name):
    reader = makeReader(file_name)
    assert reader.__class__.__name__ == expected_class_name

def test_makeReader_unsupported_extension():
    with pytest.raises(ValueError):
        makeReader("unknown.xyz")