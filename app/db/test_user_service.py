import pytest
from base64 import b32encode
from .arangodb import ArangoDatabase
from .users_service import UserDBService
from ..schema.users import NewUser
from .theExceptions import EmailNotFoundError


def test_find_user():
    db = ArangoDatabase()
    userService = UserDBService(db)

    with pytest.raises(EmailNotFoundError):
        email = "test@test.fr"
        user = userService.find_user(email)
        assert user.email == email


def test_check_constraint_before_create_user():
    db = ArangoDatabase()
    userService = UserDBService(db)

    try:
        new_user = NewUser(
            username="test", email="test@sfr.fr", password="12345678")

        userService.check_constraint_before_create_user(new_user)
    except EmailNotFoundError as emailExc:
        assert False, f"'check_constraint_before_create_user' raised an exception {emailExc}"
    except Exception as exc:
        assert False, f"'check_constraint_before_create_user' raised an exception {exc}"


def test_create_user():
    db = ArangoDatabase().instance
    userService = UserDBService(db)

    try:
        new_user = NewUser(
            username="test", email="test@sfr.fr", password="12345678")

        userService.create_user(new_user)
    except Exception as exc:
        assert False, f"'create_user' raised an exception {exc}"


def test_create_user_session():
    db = ArangoDatabase().instance
    userService = UserDBService(db)
    try:
        user_key = "260295"
        sid = b32encode(user_key.encode("UTF-8")).decode("utf-8")
        userService.create_user_session(user_key, sid)
    except Exception as exc:
        assert False, f"'create_user_session' raised an exception {exc}"


def test_delete_session():
    db = ArangoDatabase().instance
    userService = UserDBService(db)
    try:
        username = "test"
        userService.delete_user(username)
    except Exception as exc:
        assert False, f"'test_delete_session' raised an exception {exc}"
