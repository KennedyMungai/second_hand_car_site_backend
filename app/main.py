"""The entrypoint to the backend application
"""
import os

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Body, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from routers.cars import cars

from models.car_model import CarBase

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


@app.get("/", tags=['Home'])
async def root():
    """The root endpoint

    Returns:
        dict[str, str]: A dictionary containing strings
    """
    return {"message": "Hello World"}

app.include_router(cars)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0000000", port=8000, reload=True)
