from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.infrastructure.models.base import Base

class GeneratedDocumentModel(Base):
    __tablename__ = "generated_documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_type_id = Column(Integer, ForeignKey("document_types.id"), nullable=False)
    file_path_or_key = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return (f"<GeneratedDocumentModel(id={self.id}, user_id={self.user_id}, "
                f"document_type_id={self.document_type_id}, file_path_or_key='{self.file_path_or_key}', "
                f"created_at={self.created_at}, expires_at={self.expires_at})>")