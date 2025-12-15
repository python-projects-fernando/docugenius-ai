from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.infrastructure.models.base import Base


class DocumentFieldModel(Base):
    __tablename__ = "document_fields"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_type_id = Column(Integer, ForeignKey("document_types.id"), nullable=False)
    name = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False)
    is_required = Column(Boolean, nullable=False, default=False)
    description = Column(String(500), nullable=True)

    def __repr__(self) -> str:
        return (f"<DocumentFieldModel(id={self.id}, document_type_id={self.document_type_id}, name='{self.name}', "
                f"field_type='{self.field_type}', is_required={self.is_required})>")