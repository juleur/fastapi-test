from pyArango.database import Database
from pyArango.connection import Connection


class ArangoDatabase:
    instance: Database

    def __init__(self) -> None:
        conn = Connection()
        self.instance = conn["_system"]
