import pytest
from backend.core.models.document_field import DocumentField
from backend.core.enums.field_type_enum import FieldType

class TestDocumentField:

    @pytest.fixture
    def valid_document_field_data(self):
        return {
            "id": 1,
            "document_type_id": 101,
            "name": "Contract Value",
            "field_type": FieldType.DECIMAL,
            "is_required": True,
            "description": "The monetary value of the contract."
        }

    def test_create_document_field_with_valid_data(self, valid_document_field_data):
        doc_field = DocumentField(**valid_document_field_data)
        assert doc_field.id == valid_document_field_data["id"]
        assert doc_field.document_type_id == valid_document_field_data["document_type_id"]
        assert doc_field.name == valid_document_field_data["name"]
        assert doc_field.field_type == valid_document_field_data["field_type"]
        assert doc_field.is_required == valid_document_field_data["is_required"]
        assert doc_field.description == valid_document_field_data["description"]

    def test_eq_with_same_id(self, valid_document_field_data):
        doc_field1 = DocumentField(**valid_document_field_data)
        data2 = valid_document_field_data.copy()
        data2["name"] = "Different Name"
        data2["description"] = "Different description."
        doc_field2 = DocumentField(**data2)
        assert doc_field1 == doc_field2
        assert doc_field2 == doc_field1

    def test_eq_with_none_id_and_same_attributes(self, valid_document_field_data):
        data1 = valid_document_field_data.copy()
        data1["id"] = None
        doc_field1 = DocumentField(**data1)
        data2 = valid_document_field_data.copy()
        data2["id"] = None
        doc_field2 = DocumentField(**data2)
        assert doc_field1 == doc_field2
        assert doc_field2 == doc_field1

    def test_eq_with_different_id(self, valid_document_field_data):
        doc_field1 = DocumentField(**valid_document_field_data)
        data2 = valid_document_field_data.copy()
        data2["id"] = 999
        doc_field2 = DocumentField(**data2)
        assert doc_field1 != doc_field2
        assert doc_field2 != doc_field1

    def test_eq_with_none_id_and_different_attributes(self, valid_document_field_data):
        data1 = valid_document_field_data.copy()
        data1["id"] = None
        data1["name"] = "name_one"
        doc_field1 = DocumentField(**data1)
        data2 = valid_document_field_data.copy()
        data2["id"] = None
        data2["name"] = "name_two"
        doc_field2 = DocumentField(**data2)
        assert doc_field1 != doc_field2
        assert doc_field2 != doc_field1

    def test_eq_with_different_type(self, valid_document_field_data):
        doc_field = DocumentField(**valid_document_field_data)
        other_obj = "Not a DocumentField"
        assert doc_field != other_obj

    def test_hash_with_same_id(self, valid_document_field_data):
        doc_field1 = DocumentField(**valid_document_field_data)
        data2 = valid_document_field_data.copy()
        data2["name"] = "Different Name"
        data2["description"] = "Different description."
        doc_field2 = DocumentField(**data2)
        assert hash(doc_field1) == hash(doc_field2)

    def test_hash_with_none_id_and_same_attributes(self, valid_document_field_data):
        data1 = valid_document_field_data.copy()
        data1["id"] = None
        doc_field1 = DocumentField(**data1)
        data2 = valid_document_field_data.copy()
        data2["id"] = None
        doc_field2 = DocumentField(**data2)
        assert hash(doc_field1) == hash(doc_field2)

    def test_hash_with_different_id(self, valid_document_field_data):
        doc_field1 = DocumentField(**valid_document_field_data)
        data2 = valid_document_field_data.copy()
        data2["id"] = 999
        doc_field2 = DocumentField(**data2)
        assert hash(doc_field1) != hash(doc_field2)

    def test_hash_with_none_id_and_different_attributes(self, valid_document_field_data):
        data1 = valid_document_field_data.copy()
        data1["id"] = None
        data1["name"] = "name_one"
        doc_field1 = DocumentField(**data1)
        data2 = valid_document_field_data.copy()
        data2["id"] = None
        data2["name"] = "name_two"
        doc_field2 = DocumentField(**data2)
        assert hash(doc_field1) != hash(doc_field2)


    def test_repr_includes_attributes(self, valid_document_field_data):
        doc_field = DocumentField(**valid_document_field_data)
        repr_str = repr(doc_field)
        assert "DocumentField" in repr_str
        assert f"id={valid_document_field_data['id']}" in repr_str
        assert f"document_type_id={valid_document_field_data['document_type_id']}" in repr_str
        assert f"name='{valid_document_field_data['name']}'" in repr_str
        assert f"field_type=FieldType.DECIMAL" in repr_str
        assert f"is_required={valid_document_field_data['is_required']}" in repr_str
        assert f"description='{valid_document_field_data['description']}'" in repr_str

    def test_repr_with_none_id(self, valid_document_field_data):
        data = valid_document_field_data.copy()
        data["id"] = None
        doc_field = DocumentField(**data)
        repr_str = repr(doc_field)
        assert "DocumentField" in repr_str
        assert "id=None" in repr_str
        assert f"document_type_id={data['document_type_id']}" in repr_str
        assert f"name='{data['name']}'" in repr_str
        assert f"field_type=FieldType.DECIMAL" in repr_str
        assert f"is_required={data['is_required']}" in repr_str
        assert f"description='{data['description']}'" in repr_str