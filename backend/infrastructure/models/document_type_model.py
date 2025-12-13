from sqlalchemy import Column, Integer, String
from backend.infrastructure.models.base import Base

class DocumentTypeModel(Base):
    __tablename__ = "document_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<DocumentType(id={self.id}, name='{self.name}', description='{self.description}')>"
