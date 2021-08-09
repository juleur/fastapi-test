from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from pyArango.database import Database
from middleware.db import get_arangodb
from db.dogs_service import DogDBService
from db.theExceptions import DogNotFound

router = APIRouter()


@router.get("/dogs")
async def get_dogs(db: Database = Depends(get_arangodb)):
    try:
        dogService = DogDBService(db)
        dogs = dogService.get_dogs()

        return dogs
    except Exception:
        raise HTTPException(status_code=500)


@router.get("/dog/{name}")
async def get_dog(name: str, db: Database = Depends(get_arangodb)):
    try:
        dogService = DogDBService(db)
        dog = dogService.get_dog(name)

        return dog
    except DogNotFound:
        raise HTTPException(
            status_code=404, detail=f"Aucun chien n'a le nom: {name}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
