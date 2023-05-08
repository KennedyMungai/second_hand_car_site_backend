"""The entrypoint to the backend application
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    """The root endpoint

    Returns:
        dict[str, str]: A dictionary containing strings
    """
    return {"message": "Hello World"}