from commands.requests.property_requests import (
    GetPropertyRequest,
    CheckAvailabilityRequest,
)
from commands.response.property_response import AvailabilityResponse
from fastapi_sqlalchemy import db
from database.db_models import Property as ModelProperty
from database.db_models import Reservation as ModelReservation


def find_property_handler(request: GetPropertyRequest):
    query = db.session.query(ModelProperty).filter(
        ModelProperty.state.ilike(f"%{request.state}%"),
        ModelProperty.city.ilike(f"%{request.city}%"),
        ModelProperty.address.ilike(f"%{request.address}%"),
    )
    if request.max_price is 0:
        query = query.filter(ModelProperty.price_per_night < request.max_price)  # type: ignore

    property_list = query.all()
    return property_list


def check_availability_handler(request: CheckAvailabilityRequest):
    conflict = find_availability_conflict(
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


def find_availability_conflict(property_id, start_date, end_date, guest_quantity):
    conflict = (
        db.session.query(ModelReservation)
        .filter(
            ModelReservation.property_id == property_id,  # type: ignore
            ModelReservation.start_date < end_date,  # type: ignore
            ModelReservation.end_date > start_date,
            ModelReservation.active,
            ModelProperty.capacity >= guest_quantity,  # type: ignore
        )
        .first()
    )
    return conflict
