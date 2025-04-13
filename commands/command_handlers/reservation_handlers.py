from fastapi_sqlalchemy import db
from commands.command_handlers.property_handlers import (
    find_availability_conflict,
    find_capacity_conflict,
    valid_dates,
)
from database.db_models import Reservation as ModelReservation
from sqlalchemy import or_
from fastapi import HTTPException


def find_reservation_handler(property_id, client_email):
    response = (
        db.session.query(ModelReservation)
        .filter(
            or_(
                ModelReservation.property_id == property_id,
                ModelReservation.client_email == client_email,
            )
        )
        .all()
    )

    if not response:
        raise HTTPException(status_code=404, detail="Item not found")

    return response


def create_reservation_handler(request):
    availability_conflict = find_availability_conflict(
        request.property_id, request.start_date, request.end_date
    )

    capacity_conflict = find_capacity_conflict(
        request.property_id, request.guest_quantity
    )

    if not valid_dates(request.start_date, request.end_date):
        raise HTTPException(status_code=400, detail="The end date precedes start date")

    if capacity_conflict:
        raise HTTPException(
            status_code=409,
            detail="The selected property doesn't support the number of guests",
        )

    if availability_conflict:
        raise HTTPException(status_code=409, detail="The date is already booked.")

    response = ModelReservation(**request.model_dump())
    db.session.add(response)
    db.session.commit()

    return response


def delete_reservation_handler(reservation_id):
    response = (
        db.session.query(ModelReservation)
        .filter(ModelReservation.id == reservation_id)  # type: ignore
        .update({"active": False})
    )
    db.session.commit()
    return response
