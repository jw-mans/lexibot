from .base_reader import Reader

class MDReader(Reader):
    def read(self, file_path: str) -> str:
        import chardet
        import markdown as md
        with open(file_path, "rb") as file:
            raw = file.read()
            encoding = chardet.detect(raw)['encoding'] or 'utf_8'
            text = raw.decode(encoding, errors='ignore')
            return md.markdown(text) # Markdown or common text?
        