from argon2 import PasswordHasher
from pydantic import EmailStr
from pyArango.database import Database
from pyArango.theExceptions import AQLQueryError
from pyArango.query import AQLQuery
from .theExceptions import EmailNotFoundError, UsernameNotFoundError
from schema.users import NewUser, UserDoc


class UserDBService():
    db: Database

    def __init__(self, arangoDB: Database) -> None:
        self.db = arangoDB

    def find_user(self, email: EmailStr) -> UserDoc:
        queryResult: AQLQuery
        try:
            aql = "FOR u IN users FILTER u.email == @email LIMIT 1 RETURN u"
            bindVars = {"email": email}
            queryResult = self.db.AQLQuery(aql, rawResults=False,
                                           batchSize=1, bindVars=bindVars)
        except:
            raise Exception

        if len(queryResult) == 0:
            raise EmailNotFoundError

        col = queryResult[0]

        user = UserDoc()
        user._id = col["_id"]
        user._key = col["_key"]
        user._rev = col["_rev"]
        user.username = col["username"]
        user.email = col["email"]
        user.hpwd = col["hpwd"]

        return user

    def create_user(self, new_user: NewUser) -> None:
        try:
            ph = PasswordHasher()
            hpwd = ph.hash(new_user.password)
            aql = "INSERT { username: @username, email: @email, hpwd: @hpwd } IN users"
            bindVars = {"username": new_user.username,
                        "email": new_user.email, "hpwd": hpwd}
            _ = self.db.AQLQuery(aql, rawResults=False,
                                 batchSize=1, bindVars=bindVars)
        except:
            raise Exception

    def check_constraint_before_create_user(self, new_user: NewUser) -> None:
        queryResult: AQLQuery
        try:
            aql = """
              LET emailExists = (FOR u IN users FILTER u.email == @email LIMIT 1 RETURN u)
              LET usernameExists = (FOR u IN users FILTER u.username == @username LIMIT 1 RETURN u)
              RETURN {
                email: emailExists[0].email,
                username: usernameExists[0].username
              }
            """
            bindVars = {"email": new_user.email, "username": new_user.username}
            queryResult = self.db.AQLQuery(aql, rawResults=False,
                                           batchSize=1, bindVars=bindVars)
        except:
            raise Exception

        if queryResult.response["result"][0]["email"] is not None:
            raise EmailNotFoundError
        if queryResult.response["result"][0]["username"] is not None:
            raise UsernameNotFoundError

    def create_user_session(self, user_doc_key: str, session_id: str):
        try:
            aql = """
              UPSERT { _key: @key }
              INSERT { _key: @key, user: @userID }
              UPDATE { _key: @key } IN sessions
            """
            bindVars = {"key": session_id,
                        "userID": f"users/{user_doc_key}"}
            _ = self.db.AQLQuery(aql, rawResults=False,
                                 batchSize=1, bindVars=bindVars)
        except AQLQueryError:
            raise Exception

    def delete_user(self, username: str):
        try:
            aql = """
              FOR u IN users
                FILTER u.username == @username
                LIMIT 1
                REMOVE { _key: u._key } IN users
                FOR s IN sessions
                  FILTER s.user == u._id
                  LIMIT 1
                  REMOVE { _key: s._key } IN sessions
                RETURN u
            """
            bindVars = {"username": username}
            _ = self.db.AQLQuery(aql, rawResults=False,
                                 batchSize=1, bindVars=bindVars)
        except AQLQueryError:
            raise Exception
