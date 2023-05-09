"""The cars router file"""
from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    car = jsonable_encoder(car)
    new_car = await request.app.mongodb["cars1"].insert_one(car)
    created_car = await request.app.mongodb["cars1"].find_one({"_id": new_car.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)
