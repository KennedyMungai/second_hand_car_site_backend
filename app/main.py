"""The entrypoint to the backend application
"""
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """The root endpoint

    Returns:
        dict[str, str]: A dictionary containing strings
    """
    return {"message": "Hello World"}
