from typing import Dict, List

class HistoryStore:
    def __init__(self):
        self.sessions: Dict[int, List[dict]] = {}

    def add_message(self, user_id: int, role: str, text: str):
        self.sessions.setdefault(user_id, []).append({
            "role": role,
            "content": text,
        })

    def get_history(self, user_id: int) -> List[dict]:
        return self.sessions.get(user_id, [])

    def clear(self, user_id: int):
        if user_id in self.sessions:
            del self.sessions[user_id]
