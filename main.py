import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import or_

from database.db_schema import Property as SchemaProperty
from database.db_schema import Reservation as SchemaReservation

from database.db_models import Property as ModelProperty
from database.db_models import Reservation as ModelReservation

from service import property_service
from commands.requests.property_requests import AvailabilityRequest
from commands.response.property_response import AvailabilityResponse

import os
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# add commands design pattern to endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to South lake zone API"}


@app.post(
    "/property/",
    response_model=SchemaProperty,
    tags=["Property Management"],
    status_code=201,
)
async def property(property: SchemaProperty):
    db_property = ModelProperty(
        title=property.title,
        address=property.address,
        city=property.city,
        state=property.state,
        country=property.country,
        capacity=property.capacity,
        price_per_night=property.price_per_night,
        active=property.active,
    )
    db.session.add(db_property)
    db.session.commit()
    return db_property


@app.get("/property/", tags=["Property Management"])
async def property(address="", city="", state="", max_price=None):
    query = db.session.query(ModelProperty).filter(
        ModelProperty.state.ilike(f"%{state}%"),
        ModelProperty.city.ilike(f"%{city}%"),
        ModelProperty.address.ilike(f"%{address}%"),
    )

    if max_price is not None:
        query = query.filter(ModelProperty.price_per_night < max_price)

    property = query.all()

    return property


@app.get(
    "/property/availability/",
    response_model=AvailabilityResponse,
    tags=["Property Management"],
)
async def availability(request: AvailabilityRequest = Depends()):
    # Depends() method makes the endpoint expect a query string instead of a body, since get endpoints can't have body

    conflict = property_service.find_avaliability_conflict(
        request.property_id,
        request.start_date,
        request.end_date,
        request.guest_quantity,
    )
    # also checking if reservation is active

    response = AvailabilityResponse(
        stay_duration=(request.end_date - request.start_date).days,
        available=not conflict,
        message=(
            "The date is available."
            if conflict is None
            else "The date is already booked."
        ),
    )

    return response


@app.post(
    "/reservation/",
    response_model=SchemaReservation,
    tags=["Reservation Management"],
    status_code=201,
)
# make required parameters required
async def reservation(reservation: SchemaReservation):
    db_reservation = ModelReservation(
        property_id=reservation.property_id,
        client_name=reservation.client_name,
        client_email=reservation.client_email,
        guest_quantity=reservation.guest_quantity,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
        active=reservation.active,
    )
    db.session.add(db_reservation)
    db.session.commit()
    return db_reservation


@app.get("/reservation/", tags=["Reservation Management"])
async def reservation(property_id=None, client_email=""):
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
async def reservation(reservation_id):
    reservation = (
        db.session.query(ModelReservation)
        .filter(ModelReservation.id == reservation_id)
        .update({"active": False})
    )
    db.session.commit()
    return reservation


# To run locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
