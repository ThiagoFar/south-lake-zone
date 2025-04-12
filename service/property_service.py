from fastapi_sqlalchemy import DBSessionMiddleware, db
from database.db_models import Property as ModelProperty
from database.db_models import Reservation as ModelReservation

def find_avaliability_conflict(property_id, start_date, end_date, guest_quantity):
    conflict = db.session.query(ModelReservation).filter(
        ModelReservation.property_id == property_id,
        ModelReservation.start_date < end_date,
        ModelReservation.end_date > start_date, ModelReservation.active, ModelProperty.capacity >= guest_quantity
    ).first()
    return conflict
