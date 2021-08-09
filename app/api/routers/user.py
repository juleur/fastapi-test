from base64 import b32encode
from argon2 import PasswordHasher
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pyArango.database import Database
from middleware.db import get_arangodb
from db.users_service import UserDBService
from schema.users import AuthUser, NewUser
from db.theExceptions import EmailNotFoundError, PasswordTooShortError, WrongCredentialsError

router = APIRouter()


@router.post("/auth")
async def auth_user(request: Request, auth_user: AuthUser, db: Database = Depends(get_arangodb)):
    try:
        userService = UserDBService(db)

        user = userService.find_user(auth_user.email)

        ph = PasswordHasher()
        match = ph.verify(user.hpwd, auth_user.password)
        if not match:
            raise WrongCredentialsError

        sid = b32encode(user._key.encode("UTF-8")).decode("utf-8")

        userService.create_user_session(user._key, sid)

        resp = Response()
        resp.set_cookie(key="sid", value=sid,
                        httponly=True, samesite="lax", domain=request.headers.get("origin"))
        resp.status_code = 202

        return resp
    except (EmailNotFoundError, WrongCredentialsError):
        raise HTTPException(
            status_code=404, detail="l'email et/ou le mot de passe sont incorrect")
    except Exception:
        raise HTTPException(status_code=500)


@router.post("/create_user")
async def create_user(new_user: NewUser, db: Database = Depends(get_arangodb)):
    try:
        if len(new_user.password) < 8:
            raise PasswordTooShortError

        userService = UserDBService(db)

        userService.check_constraint_before_create_user(new_user)
        userService.create_user(new_user)

        return JSONResponse({"msg": f"votre compte, {new_user.username} a bien été créé"}, status_code=202)
    except PasswordTooShortError:
        raise HTTPException(
            status_code=422, detail="votre mot de passe est trop court")
    except Exception:
        raise HTTPException(status_code=500)


@router.delete("/{username}")
async def delete_user(username: str, db: Database = Depends(get_arangodb)):
    try:
        userService = UserDBService(db)
        userService.delete_user(username)
        return Response(status_code=202)
    except:
        raise HTTPException(status_code=500)
