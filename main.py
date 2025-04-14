import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db

from commands.command_handlers.property_handlers import (
    find_property_handler,
    check_availability_handler,
)
from commands.command_handlers.reservation_handlers import (
    find_reservation_handler,
    delete_reservation_handler,
    create_reservation_handler,
)

from database.db_schema import Property as SchemaProperty
from database.db_schema import Reservation as SchemaReservation
from database.db_models import Property as ModelProperty

from commands.requests.property_requests import (
    CheckAvailabilityRequest,
    GetPropertyRequest,
)
from commands.response.property_response import AvailabilityResponse


load_dotenv(".env")
load_dotenv()
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])  # type: ignore


@app.get("/")
async def root():
    return {"message": "Welcome to South lake zone API"}


# fmt:off
@app.post("/property/", response_model=SchemaProperty, tags=["Property Management"], status_code=201)# fmt:on
async def create_property(request: SchemaProperty):
    response = ModelProperty(**request.model_dump())
    db.session.add(response)
    db.session.commit()
    return response


@app.get("/property/", tags=["Property Management"])
async def find_property(request: GetPropertyRequest = Depends()):
    response = find_property_handler(request)
    return response

# fmt:off
@app.get("/property/availability/", response_model=AvailabilityResponse, tags=["Property Management"])# fmt:on
async def check_availability(
    request: CheckAvailabilityRequest = Depends()):
    response = check_availability_handler(request)
    return response


# fmt:off
@app.post("/reservation/", response_model=SchemaReservation, tags=["Reservation Management"], status_code=201)# fmt:on
async def create_reservation(request: SchemaReservation):
    response = create_reservation_handler(request)
    return response


@app.get("/reservation/", tags=["Reservation Management"])
async def find_reservation(property_id=None, client_email=""):
    response = find_reservation_handler(property_id, client_email)
    return response


@app.delete("/reservation/", tags=["Reservation Management"])
async def delete_reservation(reservation_id):
    response = delete_reservation_handler(reservation_id)
    return response


# To run locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
