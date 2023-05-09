"""The cars router file"""
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.car_model import CarBase, CarDB

cars = APIRouter(prefix='/cars', tags=['Cars'])


@cars.get("/", response_description="List all cars")
async def list_cars(
        request: Request,
        min_price: int = 0,
        max_price: int = 100000,
        brand: Optional[str] = None
) -> List[CarDB]:
    """An endpoint to list all cars in the database

    Returns:
        List[CarDB]: A list of all cars
    """
    query = {"price": {"$lt": max_price, "$gt": min_price}}

    if brand:
        query["brand"] = brand

    full_query = request.app.mongodb["cars1"].find(query).sort("_id", 1)

    results = [CarDB(**raw_car) async for raw_car in full_query]

    return results


@cars.post("/", response_description="Create a new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    """This is an endpoint that creates a car

    Args:
        request (Request): A request object
        car (CarBase, optional): The template for the Car data. Defaults to Body(...).

    Returns:
        JSONResponse: The response is in JSON format
    """
    car = jsonable_encoder(car)
    new_car = await request.app.mongodb["cars1"].insert_one(car)
    created_car = await request.app.mongodb["cars1"].find_one({"_id": new_car.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@cars.get("/{car_id}", response_description="Get a car by id")
async def show_car(car_id: str, request: Request):
    """Returned a single car from the database based on its ID

    Args:
        car_id (str): The Id of the car
        request (Request): The request object

    Raises:
        HTTPException: Raises a 404 not found if not found
    """
    if (car := await request.app.mongodb["cars1"].find_one({"_id": car_id})) is not None:
        return CarDB(**car)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Car with {car_id} not found")
