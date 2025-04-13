from fastapi_sqlalchemy import db
from commands.requests.property_requests import GetPropertyRequest
from database.db_models import Property as ModelProperty

def get_property_handler(request: GetPropertyRequest):
    query = db.session.query(ModelProperty).filter(
        ModelProperty.state.ilike(f"%{request.state}%"),
        ModelProperty.city.ilike(f"%{request.city}%"),
        ModelProperty.address.ilike(f"%{request.address}%"),
    )
    if request.max_price is 0:
        query = query.filter(ModelProperty.price_per_night < request.max_price)  # type: ignore

    property_list = query.all()
    return property_list
