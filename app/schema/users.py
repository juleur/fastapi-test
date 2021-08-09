from pydantic.main import BaseModel
from pydantic import EmailStr


class AuthUser(BaseModel):
    email: EmailStr
    password: str


class NewUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDoc():
    _id: str
    _key: str
    _rev: str
    username: str
    email: EmailStr
    hpwd: str

    def __repr__(self):
        return str(self.__dict__)
