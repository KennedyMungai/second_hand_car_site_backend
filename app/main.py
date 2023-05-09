"""The entrypoint to the backend application
"""
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

app = FastAPI()
load_dotenv(find_dotenv())

DB_NAME = os.environ.get("DB_NAME")
DB_URL = os.environ.get("DB_URL")


@app.get("/")
async def root():
    """The root endpoint

    Returns:
        dict[str, str]: A dictionary containing strings
    """
    return {"message": "Hello World"}
