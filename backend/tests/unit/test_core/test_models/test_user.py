import pytest
from datetime import datetime, timezone
from backend.core.models.user import User
from backend.core.value_objects.hashed_password import HashedPassword

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
            "role": "common",
            "is_active": True,
            "created_at": datetime(2023, 1, 1, tzinfo=timezone.utc),
            "updated_at": datetime(2023, 1, 1, tzinfo=timezone.utc)
        }

    def test_create_user_with_valid_data(self, valid_user_data):
        user = User(**valid_user_data)
        assert user.id == valid_user_data["id"]
        assert user.username == valid_user_data["username"]
        assert user.email == valid_user_data["email"]
        assert user.hashed_password == valid_user_data["hashed_password"]
        assert user.role == valid_user_data["role"]
        assert user.is_active == valid_user_data["is_active"]
        assert user.created_at == valid_user_data["created_at"]
        assert user.updated_at == valid_user_data["updated_at"]

    def test_create_user_without_optional_fields_defaults_correctly(self, valid_hashed_password):
        user = User(
            id=2,
            username="anotheruser",
            email="anotheruser@example.com",
            hashed_password=valid_hashed_password,
        )
        assert user.role == "common"
        assert user.is_active is True

    def test_create_user_sets_timestamps_if_not_provided(self, valid_hashed_password):
        user = User(id=3, username="timeuser", email="timeuser@example.com", hashed_password=valid_hashed_password)
        assert user.created_at is not None
        assert user.updated_at is not None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.created_at.tzinfo == timezone.utc
        assert user.updated_at.tzinfo == timezone.utc

    @pytest.mark.parametrize("invalid_username", ["", "   ", "\t\n"])
    def test_create_user_with_invalid_username_raises_value_error(self, invalid_username, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=4,
                username=invalid_username,
                email="valid@example.com",
                hashed_password=valid_hashed_password
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_create_user_with_none_username_raises_value_error(self, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=5,
                username=None,
                email="valid@example.com",
                hashed_password=valid_hashed_password
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_email", ["", "   ", "\t\n"])
    def test_create_user_with_invalid_email_raises_value_error(self, invalid_email, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=6,
                username="validuser",
                email=invalid_email,
                hashed_password=valid_hashed_password
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_create_user_with_none_email_raises_value_error(self, valid_hashed_password):
        with pytest.raises(ValueError) as exc_info:
            User(
                id=7,
                username="validuser",
                email=None,
                hashed_password=valid_hashed_password
            )
        assert "cannot be empty or just whitespace" in str(exc_info.value)

    def test_username_is_stripped_after_init(self, valid_hashed_password):
        username_with_spaces = "  testuser  "
        expected_username = "testuser"
        user = User(
            id=8,
            username=username_with_spaces,
            email="valid@example.com",
            hashed_password=valid_hashed_password
        )
        assert user.username == expected_username

    def test_email_is_stripped_after_init(self, valid_hashed_password):
        email_with_spaces = "  valid@example.com  "
        expected_email = "valid@example.com"
        user = User(
            id=9,
            username="validuser",
            email=email_with_spaces,
            hashed_password=valid_hashed_password
        )
        assert user.email == expected_email

    def test_eq_with_same_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["username"] = "different_username"
        user2_data["email"] = "different@example.com"
        user2 = User(**user2_data)
        assert user1 == user2
        assert user2 == user1

    def test_eq_with_none_id_and_same_attributes(self, valid_hashed_password):
        user1 = User(
            id=None,
            username="samename",
            email="same@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        user2 = User(
            id=None,
            username="samename",
            email="same@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        assert user1 == user2
        assert user2 == user1

    def test_eq_with_different_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["id"] = 99
        user2 = User(**user2_data)
        assert user1 != user2
        assert user2 != user1

    def test_eq_with_none_id_and_different_attributes(self, valid_hashed_password):
        user1 = User(
            id=None,
            username="name1",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True
        )
        user2 = User(
            id=None,
            username="name2",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True
        )
        assert user1 != user2
        assert user2 != user1

        user3 = User(
            id=None,
            username="name1",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="admin",
            is_active=True
        )
        user4 = User(
            id=None,
            username="name1",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True
        )
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

    def test_hash_with_none_id_and_same_attributes(self, valid_hashed_password):
        user1 = User(
            id=None,
            username="samename",
            email="same@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        user2 = User(
            id=None,
            username="samename",
            email="same@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True,
            created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2023, 1, 1, tzinfo=timezone.utc)
        )
        assert hash(user1) == hash(user2)

    def test_hash_with_different_id(self, valid_user_data):
        user1 = User(**valid_user_data)
        user2_data = valid_user_data.copy()
        user2_data["id"] = 99
        user2 = User(**user2_data)
        assert hash(user1) != hash(user2)

    def test_hash_with_none_id_and_different_attributes(self, valid_hashed_password):
        user1 = User(
            id=None,
            username="name1",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True
        )
        user2 = User(
            id=None,
            username="name2",
            email="email1@example.com",
            hashed_password=valid_hashed_password,
            role="common",
            is_active=True
        )
        assert hash(user1) != hash(user2)