from dataclasses import dataclass

@dataclass
class Bookmark:
    label: str
    timestamp: int
    filepath: str

