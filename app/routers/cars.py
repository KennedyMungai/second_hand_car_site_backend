"""The cars router file"""
from fastapi import APIRouter, Body, Request

from models.car_model import CarBase

cars = APIRouter(prefix='/cars', tags=['Cars'])


@cars.get("/", response_description="List all cars")
async def list_cars():
    """An endpoint to list all cars in the database

    Returns:
        dict[str, str]: A simple placeholder message
    """
    return {"data": "All cars will go here"}


@cars.post("/", response_description="Create a new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    pass
