from fastapi_sqlalchemy import db

from commands.response.property_response import AvailabilityResponse
from database.db_models import Reservation as ModelReservation
from sqlalchemy import or_
from fastapi import HTTPException

from service import property_service


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
    conflict = property_service.find_availability_conflict(
        request.property_id,
        request.start_date,
        request.end_date,
        request.guest_quantity
    )

    if conflict:
        raise HTTPException(status_code=409, detail="The selected date is already booked.")




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

