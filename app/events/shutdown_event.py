import sys
from db.arangodb import ArangoDatabase


def drop_arangodb_collections() -> None:
    try:
        db = ArangoDatabase()
        _ = db.instance.dropAllCollections()
    except Exception:
        sys.exit(1)
