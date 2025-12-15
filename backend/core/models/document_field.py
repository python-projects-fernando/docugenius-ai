from dataclasses import dataclass
from typing import Optional

@dataclass
class DocumentField:
    id: Optional[int]
    document_type_id: int
    name: str
    field_type: str
    is_required: bool
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("DocumentField name cannot be empty or just whitespace.")
        if not self.field_type or not self.field_type.strip():
            raise ValueError("DocumentField field_type cannot be empty or just whitespace.")
        self.name = self.name.strip()
        self.field_type = self.field_type.strip()
        if self.description:
            self.description = self.description.strip()

    def __eq__(self, other):
        if not isinstance(other, DocumentField):
            return False
        if self.id is not None and other.id is not None:
            return self.id == other.id
        return (
            self.document_type_id == other.document_type_id
            and self.name == other.name
            and self.field_type == other.field_type
            and self.is_required == other.is_required
            and self.description == other.description
        )

    def __hash__(self):
        if self.id is not None:
            return hash(self.id)
        return hash((
            self.document_type_id,
            self.name,
            self.field_type,
            self.is_required,
            self.description
        ))

    def __repr__(self):
        return (
            f"DocumentField("
            f"id={self.id}, "
            f"document_type_id={self.document_type_id}, "
            f"name='{self.name}', "
            f"field_type='{self.field_type}', "
            f"is_required={self.is_required}, "
            f"description='{self.description}'"
            f")"
        )