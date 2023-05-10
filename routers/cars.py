"""The cars router file"""
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth.authentication import AuthHandler
from models.car_model import CarBase, CarDB, CarUpdate

cars_router = APIRouter(prefix='/cars', tags=['Cars'])
auth_handler = AuthHandler()


@cars_router.get("/", response_description="List all cars")
async def list_all_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1
) -> List[CarDB]:
    """Lists all the cars in the database

    Args:
        request (Request): The request object
        min_price (int, optional): The minimum price. Defaults to 0.
        max_price (int, optional): The maximum price. Defaults to 100000.
        brand (Optional[str], optional): The brand of the car. Defaults to None.

    Returns:
        List[CarDB]: A list of cars in the database.

    """
    RESULTS_PER_PAGE = 25
    skip = (page - 1)*RESULTS_PER_PAGE
    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    full_query = request.app.mongodb['cars1'].find(query).sort(
        "_id", -1).skip(skip).limit(RESULTS_PER_PAGE)

    results = [CarDB(**raw_car) async for raw_car in full_query]

    return results


@cars_router.post("/", response_description="Create a new car")
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


@cars_router.get("/{car_id}", response_description="Get a car by id")
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


@cars_router.patch("/{car_id}", response_description="Update a car by id")
async def update_task(
    car_id: str,
    request: Request,
    CarUpdate=Body(...)
):
    """The car update endpoint

    Args:
        car_id (str): The id of the car record
        request (Request): The request object
        CarUpdate (_type_, optional): The template for updating the car data. Defaults to Body(...).

    Raises:
        HTTPException: Raises a 404 not found if not found

    Returns:
        CarDb: The info on the updated car using the appropriate template
    """
    await request.app.mongodb["cars1"].update_one({"_id": car_id}, {"$set": car.dict(exclude_unset=True)})

    if (car := await request.app.mongodb["cars1"].find_one({"_id": car_id})) is not None:
        return CarDB(**car)

    return CarDB(**car)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Car with {car_id} not found")


@cars_router.delete("/{car_id}", response_description="Delete a car by id")
async def delete_car(car_id: str, request: Request):
    """The delete car endpoint

    Args:
        car_id (str): The id of the car
        request (Request): The request object

    Raises:
        HTTPException: The exception defined in the library

    Returns:
        JSONResponse: The response is in JSON format
    """
    delete_result = await request.app.mongodb["cars1"].delete_one({"_id": car_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Car with {car_id} not found")
