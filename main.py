import os
import uvicorn
from sqlalchemy import or_
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from service import property_service

from database.db_schema import Property as SchemaProperty
from database.db_schema import Reservation as SchemaReservation
from database.db_models import Property as ModelProperty
from database.db_models import Reservation as ModelReservation

from commands.requests.property_requests import AvailabilityRequest
from commands.response.property_response import AvailabilityResponse


load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])  # type: ignore


@app.get("/")
async def root():
    return {"message": "Welcome to South lake zone API"}


# fmt:off
@app.post("/property/", response_model=SchemaProperty, tags=["Property Management"], status_code=201)# fmt:on
async def create_property(request: SchemaProperty):
    db_property = ModelProperty(**request.model_dump())
    db.session.add(db_property)
    db.session.commit()
    return db_property


@app.get("/property/", tags=["Property Management"])
async def find_property(address="", city="", state="", max_price=None):
    query = db.session.query(ModelProperty).filter(
        ModelProperty.state.ilike(f"%{state}%"),
        ModelProperty.city.ilike(f"%{city}%"),
        ModelProperty.address.ilike(f"%{address}%"),
    )
    if max_price is not None:
        query = query.filter(ModelProperty.price_per_night < max_price)  # type: ignore

    property_list = query.all()
    return property_list

# fmt:off
@app.get("/property/availability/", response_model=AvailabilityResponse, tags=["Property Management"])# fmt:on
async def check_availability(
    request: AvailabilityRequest = Depends(),
):  # Depends() method makes the endpoint expect a query string instead of a body, since get endpoints can't have body
    conflict = property_service.find_avaliability_conflict(
        request.property_id,
        request.start_date,
        request.end_date,
        request.guest_quantity,
    )
    # fmt:off
    response = AvailabilityResponse(
        stay_duration=(request.end_date - request.start_date).days,
        available=not conflict,
        message=("The date is available." if conflict is None else "The date is already booked."
        ),
    )
    # fmt:on

    return response


# fmt:off
@app.post("/reservation/", response_model=SchemaReservation, tags=["Reservation Management"], status_code=201)# fmt:on
async def create_reservation(request: SchemaReservation):
    db_reservation = ModelReservation(**request.model_dump())
    db.session.add(db_reservation)
    db.session.commit()
    return db_reservation


@app.get("/reservation/", tags=["Reservation Management"])
async def find_reservation(property_id=None, client_email=""):

    reservation = (
        db.session.query(ModelReservation)
        .filter(
            or_(
                ModelReservation.property_id == property_id,
                ModelReservation.client_email == client_email,
            )
        )
        .all()
    )

    if not reservation:
        raise HTTPException(status_code=404, detail="Item not found")
    return reservation


@app.delete("/reservation/", tags=["Reservation Management"])
async def delete_reservation(reservation_id):
    reservation = (
        db.session.query(ModelReservation)
        .filter(ModelReservation.id == reservation_id)  # type: ignore
        .update({"active": False})
    )
    db.session.commit()
    return reservation


# To run locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
