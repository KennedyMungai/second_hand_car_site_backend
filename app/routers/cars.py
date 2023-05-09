"""The cars router file"""
from fastapi import APIRouter

cars = APIRouter(prefix='cars', tags=['cars'])


@cars.get("/", response_description="List all cars")
async def list_cars():
    """An endpoint to list all cars in the database

    Returns:
        dict[str, str]: A simple placeholder message
    """
    return {"data": "All cars will go here"}
