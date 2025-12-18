import pytest
from backend.core.models.user import User
from backend.core.value_objects.hashed_password import HashedPassword
from backend.core.enums.user_role_enum import UserRole

class TestUser:

    @pytest.fixture
    def valid_hashed_password(self):
        return HashedPassword(value="$2b$12$LQv3c2Y5Z4p3q8N6v7Y9z.Xi3k4l5m6n7o8p9q0r1s2t3u4v5w6x7")

    @pytest.fixture
    def valid_user_data(self, valid_hashed_password):
        return {
            "id": 1,
            "username": "testuser",
            "email": "testuser@example.com",
            "hashed_password": valid_hashed_password,
            "role": UserRole.COMMON_USER,
            "is_active": True,
        }

    def test_create_user_with_valid_data(self, valid_user_data, valid_hashed_password):
        user = User(**valid_user_data)
        assert user.id == valid_user_data["id"]
        assert user.username == valid_user_data["username"]
        assert user.email == valid_user_data["email"]
        assert user.hashed_password == valid_user_data["hashed_password"]
        assert user.role == valid_user_data["role"]
        assert user.is_active == valid_user_data["is_active"]
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_create_user_without_optional_fields_defaults_correctly(self, valid_hashed_password):
        user_data = {
            "id": 2,
            "username": "anotheruser",
            "email": "anotheruser@example.com",
            "hashed_password": valid_hashed_password,
        }

        user = User(**user_data)
        assert user.role == UserRole.COMMON_USER
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    @pytest.mark.parametrize("invalid_username", ["", "   ", "\t\n"])
    def test_create_user_with_invalid_username_raises_value_error(self, invalid_username, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=1,
                username=invalid_username,
                email="valid@example.com",
                hashed_password=valid_hashed_password,
                role=UserRole.ADMIN
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_email", ["", "   ", "\t\n"])
    def test_create_user_with_invalid_email_raises_value_error(self, invalid_email, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=1,
                username="validuser",
                email=invalid_email,
                hashed_password=valid_hashed_password,
                role=UserRole.ADMIN
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_create_user_with_invalid_role_raises_value_error(self, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=1,
                username="validuser",
                email="valid@example.com",
                hashed_password=valid_hashed_password,
                role="invalid_role_string"
            )
        assert "must be a member of UserRole Enum" in str(exc_info.value)

    def test_eq_with_same_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["username"] = "different_username"
        user2_data["email"] = "different@example.com"
        user2 = User(**user2_data)
        assert user1 == user2
        assert user2 == user1

    def test_eq_with_none_id_and_same_attributes(self, valid_user_data):
        data1 = valid_user_data.copy()
        data1["id"] = None
        user1 = User(**data1)
        data2 = valid_user_data.copy()
        data2["id"] = None
        user2 = User(**data2)
        assert user1 == user2
        assert user2 == user1

    def test_eq_with_different_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["id"] = 999
        user2 = User(**user2_data)
        assert user1 != user2
        assert user2 != user1

    def test_eq_with_none_id_and_different_attributes(self, valid_user_data):
        data1 = valid_user_data.copy()
        data1["id"] = None
        data1["username"] = "name_one"
        user1 = User(**data1)
        data2 = valid_user_data.copy()
        data2["id"] = None
        data2["username"] = "name_two"
        user2 = User(**data2)
        assert user1 != user2
        assert user2 != user1

        data3 = valid_user_data.copy()
        data3["id"] = None
        data3["role"] = UserRole.ADMIN
        user3 = User(**data3)
        data4 = valid_user_data.copy()
        data4["id"] = None
        data4["role"] = UserRole.COMMON_USER
        user4 = User(**data4)
        assert user3 != user4
        assert user4 != user3

    def test_eq_with_different_type(self, valid_user_data):
        user = User(**valid_user_data)
        other_obj = "Not a User"
        assert user != other_obj

    def test_hash_with_same_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["username"] = "different_username"
        user2_data["email"] = "different@example.com"
        user2 = User(**user2_data)
        assert hash(user1) == hash(user2)

    def test_hash_with_none_id_and_same_attributes(self, valid_user_data):
        data1 = valid_user_data.copy()
        data1["id"] = None
        user1 = User(**data1)
        data2 = valid_user_data.copy()
        data2["id"] = None
        user2 = User(**data2)
        assert hash(user1) == hash(user2)

    def test_hash_with_different_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["id"] = 999
        user2 = User(**user2_data)
        assert hash(user1) != hash(user2)

    def test_hash_with_none_id_and_different_attributes(self, valid_user_data):
        data1 = valid_user_data.copy()
        data1["id"] = None
        data1["username"] = "name_one"
        user1 = User(**data1)
        data2 = valid_user_data.copy()
        data2["id"] = None
        data2["username"] = "name_two"
        user2 = User(**data2)
        assert hash(user1) != hash(user2)

        data3 = valid_user_data.copy()
        data3["id"] = None
        data3["role"] = UserRole.ADMIN
        user3 = User(**data3)
        data4 = valid_user_data.copy()
        data4["id"] = None
        data4["role"] = UserRole.COMMON_USER
        user4 = User(**data4)
        assert hash(user3) != hash(user4)

    def test_repr_includes_attributes(self, valid_user_data):
        user = User(**valid_user_data)
        repr_str = repr(user)
        assert "User" in repr_str
        assert f"id={valid_user_data['id']}" in repr_str
        assert f"username='{valid_user_data['username']}'" in repr_str
        assert f"email='{valid_user_data['email']}'" in repr_str
        assert f"role={valid_user_data['role']}" in repr_str
        assert f"is_active={valid_user_data['is_active']}" in repr_str

    def test_repr_with_none_id(self, valid_user_data):
        data = valid_user_data.copy()
        data["id"] = None
        user = User(**data)
        repr_str = repr(user)
        assert "User" in repr_str
        assert "id=None" in repr_str
        assert f"username='{user.username}'" in repr_str
        assert f"email='{user.email}'" in repr_str
        assert f"role={user.role}" in repr_str
        assert f"is_active={user.is_active}" in repr_str