"""The entrypoint to the backend application
"""
import os

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from routers.cars import cars
from models.car_model import CarBase
from routers.users import users_router

app = FastAPI()
load_dotenv(find_dotenv())

DB_NAME = os.environ.get("DB_NAME")
DB_URL = os.environ.get("DB_URL")

origins = [
    'http://localhost',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
    uvicorn.run("main:app", reload=True)
