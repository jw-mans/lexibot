from .base_reader import Reader

class PDFReader(Reader):
    def read(self, file_path: str) -> str:
        from pypdf import PdfReader
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            return '\n'.join(page.extract_text() or "" for page in reader.pages)
        