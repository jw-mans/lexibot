from .base_reader import Reader

class RTFReader(Reader):
    def read(self, file_path: str) -> str:
        from striprtf.striprtf import (
            rtf_to_text as rtt,
        )
        with open(file_path, "r", 
            encoding="utf-8", 
            errors="ignore"
        ) as file:
            rtf_content = file.read()
            return rtt(rtf_content)
