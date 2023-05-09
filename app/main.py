"""The entrypoint to the backend application
"""
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
load_dotenv(find_dotenv())

DB_NAME = os.environ.get("DB_NAME")
DB_URL = os.environ.get("DB_URL")


@app.on_event("startup")
async def startup_db_client():
    "Defined the db connection code on start up"
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    """The logic to shutdown the mongodb connection"""
    app.mongodb_client.close()


@app.get("/")
async def root():
    """The root endpoint

    Returns:
        dict[str, str]: A dictionary containing strings
    """
    return {"message": "Hello World"}
