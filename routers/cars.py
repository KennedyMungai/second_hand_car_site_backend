"""The cars router file"""
from fastapi import APIRouter, Body, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.car_model import CarBase, CarDB

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
