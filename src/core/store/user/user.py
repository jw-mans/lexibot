import os
from pathlib import Path
from typing import Dict

class UserStore:
    def __init__(self,
        base_dir: str
    ):
        
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(
            parents=True, 
            exist_ok=True,
        )
        self.docs: Dict[int, dict] = {}

    def save_file(self,
        user_id: int,
        file_name: str,
        content: str
    ) -> str:
        
        user_dir = self.base_dir / str(user_id)
        user_dir.mkdir(
            parents=True, 
            exist_ok=True,
        )
        file_path = user_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.docs[user_id] = {
            'file_name' : file_name,
            'path' : str(file_path),
            'content': content,
        }
        return str(file_path)
    
    def get_content(self,
        user_id: int
    ) -> str:
        user_doc = self.docs.get(user_id)
        return user_doc['content'] if user_doc else ""