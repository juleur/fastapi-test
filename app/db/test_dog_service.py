import pytest
from .arangodb import ArangoDatabase
from ..db.theExceptions import DogNotFound
from .dogs_service import DogDBService


def test_get_dogs():
    db = ArangoDatabase().instance
    dogService = DogDBService(db)

    try:
        dogs = dogService.get_dogs()
    except Exception as exc:
        assert False, f"'get_dogs' raised an exception {exc}"


def test_get_dog():
    db = ArangoDatabase()
    dogService = DogDBService(db)

    try:
        dog_name = "cookie"
        dog = dogService.get_dog(dog_name)
        assert dog_name == dog.name
    except DogNotFound as dogExc:
        assert False, f"'get_dog' raised an exception {dogExc}"
    except Exception as exc:
        assert False, f"'get_dog' raised an exception {exc}"
