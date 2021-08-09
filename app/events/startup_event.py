import sys
import dognames as names
import random
from pyArango.theExceptions import CreationError
from db.arangodb import ArangoDatabase
from db.dogs_service import DogDBService


def create_arangodb_collections() -> None:
    try:
        db = ArangoDatabase()
        _ = db.instance.createCollection(name="users")
        _ = db.instance.createCollection(name="sessions")
        _ = db.instance.createCollection(name="dogs")
    except CreationError:
        pass
    except Exception:
        sys.exit(1)


def add_dog_collections() -> None:
    try:
        db = ArangoDatabase().instance
        dogService = DogDBService(db)
        maledogs = names.malearr(25)
        femaledogs = names.femalearr(25)
        all_dogs_name = [*maledogs, *femaledogs]
        random.shuffle(all_dogs_name)
        for name in all_dogs_name:
            dogService.insert_dog(name)
    except:
        sys.exit(1)
