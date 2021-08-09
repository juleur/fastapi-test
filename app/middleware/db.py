from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from db.arangodb import ArangoDatabase


class DBConnection(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.db = ArangoDatabase().instance
        response = await call_next(request)
        return response


def get_arangodb(request: Request):
    return request.state.db
