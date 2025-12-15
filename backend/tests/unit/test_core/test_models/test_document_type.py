import pytest
from backend.core.models.document_type import DocumentType

class TestDocumentType:

    def test_create_document_type_with_valid_data(self):
        id_val = 1
        name_val = "Service Contract"
        description_val = "A standard service contract template."
        doc_type = DocumentType(id=id_val, name=name_val, description=description_val)
        assert doc_type.id == id_val
        assert doc_type.name == name_val
        assert doc_type.description == description_val

    def test_create_document_type_without_description(self):
        id_val = 2
        name_val = "Commercial Proposal"
        doc_type = DocumentType(id=id_val, name=name_val, description=None)
        assert doc_type.id == id_val
        assert doc_type.name == name_val
        assert doc_type.description is None

    @pytest.mark.parametrize("invalid_name", ["", "   ", "\t\n"])
    def test_create_document_type_with_invalid_name_raises_value_error(self, invalid_name):
        with pytest.raises(ValueError) as exc_info:
            DocumentType(id=1, name=invalid_name, description="A description")
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_create_document_type_with_none_name_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            DocumentType(id=1, name=None, description="A description")
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_name_is_stripped_after_init(self):
        name_with_spaces = "  Service Contract  "
        expected_name = "Service Contract"
        doc_type = DocumentType(id=1, name=name_with_spaces, description="A description")
        assert doc_type.name == expected_name

    def test_eq_with_same_id(self):
        doc1 = DocumentType(id=1, name="A", description="Desc A")
        doc2 = DocumentType(id=1, name="B", description="Desc B")
        assert doc1 == doc2
        assert doc2 == doc1

    def test_eq_with_none_id_and_same_attributes(self):
        doc1 = DocumentType(id=None, name="A", description="Desc A")
        doc2 = DocumentType(id=None, name="A", description="Desc A")
        assert doc1 == doc2
        assert doc2 == doc1

    def test_eq_with_different_id(self):
        doc1 = DocumentType(id=1, name="A", description="Desc A")
        doc2 = DocumentType(id=2, name="A", description="Desc A")
        assert doc1 != doc2
        assert doc2 != doc1

    def test_eq_with_none_id_and_different_attributes(self):
        doc1 = DocumentType(id=None, name="A", description="Desc A")
        doc2 = DocumentType(id=None, name="B", description="Desc A")
        assert doc1 != doc2
        assert doc2 != doc1

        doc3 = DocumentType(id=None, name="A", description="Desc A")
        doc4 = DocumentType(id=None, name="A", description="Desc B")
        assert doc3 != doc4
        assert doc4 != doc3

    def test_eq_with_different_type(self):
        doc = DocumentType(id=1, name="A", description="Desc A")
        other_obj = "Not a DocumentType"
        assert doc != other_obj

    def test_hash_with_same_id(self):
        doc1 = DocumentType(id=1, name="A", description="Desc A")
        doc2 = DocumentType(id=1, name="B", description="Desc B")
        assert hash(doc1) == hash(doc2)

    def test_hash_with_none_id_and_same_attributes(self):
        doc1 = DocumentType(id=None, name="A", description="Desc A")
        doc2 = DocumentType(id=None, name="A", description="Desc A")
        assert hash(doc1) == hash(doc2)

    def test_hash_with_different_id(self):
        doc1 = DocumentType(id=1, name="A", description="Desc A")
        doc2 = DocumentType(id=2, name="A", description="Desc A")
        assert hash(doc1) != hash(doc2)

    def test_hash_with_none_id_and_different_attributes(self):
        doc1 = DocumentType(id=None, name="A", description="Desc A")
        doc2 = DocumentType(id=None, name="B", description="Desc A")
        assert hash(doc1) != hash(doc2)

    def test_repr_includes_attributes(self):
        id_val = 1
        name_val = "Service Contract"
        description_val = "A standard service contract template."
        doc_type = DocumentType(id=id_val, name=name_val, description=description_val)
        repr_str = repr(doc_type)
        assert "DocumentType" in repr_str
        assert f"id={id_val}" in repr_str
        assert f"name='{name_val}'" in repr_str
        assert f"description='{description_val}'" in repr_str

    def test_repr_with_none_description(self):
        id_val = 2
        name_val = "Commercial Proposal"
        doc_type = DocumentType(id=id_val, name=name_val, description=None)
        repr_str = repr(doc_type)
        assert "DocumentType" in repr_str
        assert f"id={id_val}" in repr_str
        assert f"name='{name_val}'" in repr_str
        assert "description='None'" in repr_str