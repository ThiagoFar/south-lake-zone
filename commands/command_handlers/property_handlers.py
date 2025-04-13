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
    if request.max_price != 0:
        query = query.filter(ModelProperty.price_per_night < request.max_price)  # type: ignore

    property_list = query.all()
    return property_list


def check_availability_handler(request: CheckAvailabilityRequest):
    availability_conflict = find_availability_conflict(
        request.property_id, request.start_date, request.end_date
    )

    capacity_conflict = find_capacity_conflict(
        request.property_id, request.guest_quantity
    )

    if not valid_dates(request.start_date, request.end_date):
        message = "The end date precedes start date"
    elif availability_conflict:
        message = "The date is already booked."
    elif capacity_conflict:
        message = "The selected property doesn't support the number of guests."
    else:
        message = "The date is available."

    # fmt:off
    response = AvailabilityResponse(
        stay_duration=(request.end_date - request.start_date).days,
        available=not availability_conflict,
        message=message
    )
    # fmt:on

    return response


def find_availability_conflict(property_id, start_date, end_date):
    conflicted_reservation = (
        db.session.query(ModelReservation)
        .filter(
            ModelReservation.property_id == property_id,  # type: ignore
            ModelReservation.start_date < end_date,  # type: ignore
            ModelReservation.end_date > start_date,  # type: ignore
            ModelReservation.active,  # type: ignore
        )
        .first()
    )
    conflict = True if conflicted_reservation is not None else False
    return conflict


def find_capacity_conflict(property_id, guest_quantity):
    property = (
        db.session.query(ModelProperty)
        .filter(
            ModelProperty.id == property_id,  # type: ignore
        )
        .first()
    )
    conflict = True if property.capacity < guest_quantity else False

    return conflict


def valid_dates(start_date, end_date):
    return not (end_date < start_date)
