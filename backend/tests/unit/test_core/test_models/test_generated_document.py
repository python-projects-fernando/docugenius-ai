import pytest
from datetime import datetime, timezone
from backend.core.models.generated_document import GeneratedDocument

class TestGeneratedDocument:

    def test_create_document_with_provided_values(self):
        user_id = 1
        doc_type_id = 2
        file_path = "path/to/document.pdf"
        created_at = datetime(2023, 10, 27, 10, 0, 0, tzinfo=timezone.utc)
        expires_at = datetime(2023, 10, 28, 10, 0, 0, tzinfo=timezone.utc)

        doc = GeneratedDocument(
            id=999,
            user_id=user_id,
            document_type_id=doc_type_id,
            file_path_or_key=file_path,
            created_at=created_at,
            expires_at=expires_at
        )

        assert doc.id == 999
        assert doc.user_id == user_id
        assert doc.document_type_id == doc_type_id
        assert doc.file_path_or_key == file_path
        assert doc.created_at == created_at
        assert doc.expires_at == expires_at

    def test_create_document_auto_sets_created_at_if_none_provided(self):
        user_id = 1
        doc_type_id = 2
        file_path = "path/to/document.pdf"

        before_creation = datetime.now(timezone.utc)

        doc = GeneratedDocument(
            id=999,
            user_id=user_id,
            document_type_id=doc_type_id,
            file_path_or_key=file_path
        )

        after_creation = datetime.now(timezone.utc)

        assert doc.created_at is not None
        assert before_creation <= doc.created_at <= after_creation
        assert doc.created_at.tzinfo == timezone.utc

    def test_create_document_with_none_id(self):
        user_id = 1
        doc_type_id = 2
        file_path = "path/to/document.pdf"

        doc = GeneratedDocument(
            id=None,
            user_id=user_id,
            document_type_id=doc_type_id,
            file_path_or_key=file_path
        )

        assert doc.id is None
        assert doc.user_id == user_id
        assert doc.document_type_id == doc_type_id
        assert doc.file_path_or_key == file_path
        assert doc.created_at is not None
        assert doc.created_at.tzinfo == timezone.utc
        assert doc.expires_at is None

    def test_entity_attributes_are_correct_type(self):
        user_id = 1
        doc_type_id = 2
        file_path = "path/to/document.pdf"
        expires_at = datetime(2023, 10, 28, 10, 0, 0, tzinfo=timezone.utc)

        doc = GeneratedDocument(
            id=999,
            user_id=user_id,
            document_type_id=doc_type_id,
            file_path_or_key=file_path,
            expires_at=expires_at
        )

        assert isinstance(doc.id, int) or doc.id is None
        assert isinstance(doc.user_id, int)
        assert isinstance(doc.document_type_id, int)
        assert isinstance(doc.file_path_or_key, str)
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.expires_at, datetime) or doc.expires_at is None

    def test_entity_is_mutable(self):
        user_id = 1
        doc_type_id = 2
        file_path = "path/to/document.pdf"

        doc = GeneratedDocument(
            id=999,
            user_id=user_id,
            document_type_id=doc_type_id,
            file_path_or_key=file_path
        )

        new_file_path = "new/path/to/document.pdf"
        doc.file_path_or_key = new_file_path

        assert doc.file_path_or_key == new_file_path