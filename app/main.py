from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from middleware.db import DBConnection
from api.routes import routers
from events.startup_event import create_arangodb_collections, add_dog_collections
from events.shutdown_event import drop_arangodb_collections

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    create_arangodb_collections()
    add_dog_collections()


@app.on_event("shutdown")
def shutdown_event():
    drop_arangodb_collections()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBConnection)
app.include_router(routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8034)
