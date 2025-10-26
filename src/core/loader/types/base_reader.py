from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> str:
        pass