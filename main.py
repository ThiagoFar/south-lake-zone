import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from db_schema import Property as SchemaProperty
from db_schema import Reservation as SchemaReservation

from db_models import Property as ModelProperty
from db_models import Reservation as ModelReservation

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

# add commands design pattern to endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to South lake zone API"}

@app.post('/property/', response_model=SchemaProperty)
async def property(property: SchemaProperty):
    db_property = ModelProperty(title = property.title, address = property.address, city = property.city, state = property.state, country = property.country, capacity = property.capacity,
                                price_per_night = property.price_per_night, active = property.active)
    db.session.add(db_property)
    db.session.commit()
    return db_property

@app.get('/property/')
async def property(address = "", city = "", state = ""):
    property = db.session.query(ModelProperty).filter(ModelProperty.state.ilike(f'%{state}%'), ModelProperty.city.ilike(f'%{city}%'), ModelProperty.address.ilike(f'%{address}%')).all()
    return property

@app.post('/reservation/', response_model=SchemaReservation)
# make required parameters required
async def reservation(reservation: SchemaReservation):
    db_reservation = ModelReservation(property_id = reservation.property_id, client_name = reservation.client_name, client_email = reservation.client_email, guest_quantity = reservation.guest_quantity,
                                      start_date = reservation.start_date, end_date = reservation.end_date,  active = reservation.active)
    db.session.add(db_reservation)
    db.session.commit()
    return db_reservation

@app.get('/reservation/')
async def reservation():
    reservation = db.session.query(ModelReservation).all()
    return reservation

@app.get('/property/avaliability/')
async def avaliability(property_id, start_date, end_date, guest_quantity):

    conflict = db.session.query(ModelReservation).filter(
        ModelReservation.property_id == property_id,
        ModelReservation.start_date < end_date,
        ModelReservation.end_date > start_date, ModelReservation.active, ModelProperty.capacity >= guest_quantity
    ).first()

    response = "AVALIABLE" if conflict is None else "UNAVALIABLE"
    return response




# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)