from .base_reader import Reader

class DocReader(Reader):
    def read(self, file_path: str) -> str:
        import docx
        with open(file_path, "rb") as file:
            doc = docx.Document(file)
            return '\n'.join(p.text for p in doc.paragraphs)
    