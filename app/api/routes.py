from fastapi import APIRouter
from .routers import user, dog

routers = APIRouter()

routers.include_router(user.router, prefix="/users", tags=["Users"])
routers.include_router(dog.router, prefix="/animals", tags=["Dogs"])
