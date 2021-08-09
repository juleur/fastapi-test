from random import randint
from typing import List
from pyArango.query import AQLQuery
from pyArango.theExceptions import AQLQueryError
from pyArango.database import Database
from schema.dogs import DogDoc
from .theExceptions import DogNotFound
from .arangodb import ArangoDatabase


class DogDBService():
    db: Database

    def __init__(self, arangoDB: ArangoDatabase) -> None:
        self.db = arangoDB

    def insert_dog(self, dog_name: str) -> None:
        try:
            age = randint(1, 17)
            aql = "INSERT { name: @dogname, age: @age } IN dogs"
            bindVars = {"dogname": dog_name, "age": age}
            _ = self.db.AQLQuery(aql, rawResults=False,
                                 batchSize=1, bindVars=bindVars)
        except AQLQueryError:
            raise Exception

    def get_dogs(self) -> List[DogDoc]:
        queryResult: AQLQuery
        try:
            aql = "FOR d IN dogs RETURN d"
            queryResult = self.db.AQLQuery(
                aql, rawResults=False, batchSize=50)
        except AQLQueryError:
            raise Exception

        if len(queryResult) == 0:
            raise Exception

        dogs: List[DogDoc] = []

        for dog in queryResult.response["result"]:
            dog_doc = DogDoc(dog["name"], dog["age"])
            dogs.append(dog_doc)

        return dogs

    def get_dog(self, name: str) -> DogDoc:
        queryResult: AQLQuery
        try:
            aql = """
              FOR d IN dogs
              FILTER d.name == name
              RETURN d
            """
            bindVars = {"name": name.capitalize()}
            queryResult = self.db.AQLQuery(aql, rawResults=False,
                                           batchSize=1, bindVars=bindVars)
        except AQLQueryError:
            raise Exception

        if len(queryResult.response.get("result")) == 0:
            raise DogNotFound

        dog = queryResult.response["result"]

        dog_doc = DogDoc(dog[0]["name"], dog[0]["age"])

        return dog_doc
