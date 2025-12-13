from dataclasses import dataclass
from typing import Optional

@dataclass
class DocumentType:
    id: Optional[int]
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("DocumentType name cannot be empty or just whitespace.")
        self.name = self.name.strip()

    def __eq__(self, other):
        if not isinstance(other, DocumentType):
            return False
        if self.id is not None and other.id is not None:
            return self.id == other.id
        return self.name == other.name and self.description == other.description

    def __hash__(self):
        if self.id is not None:
            return hash(self.id)
        return hash((self.name, self.description))

    def __repr__(self):
        return f"DocumentType(id={self.id}, name='{self.name}', description='{self.description}')"
