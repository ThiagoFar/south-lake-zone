# build a schema using pydantic
import datetime
from pydantic import BaseModel

class Property(BaseModel):
    title: str
    address: str
    city: str
    state: str
    country: str
    capacity: int
    price_per_night: int
    active: bool

    model_config = {
        "from_attributes": True
    }

class Reservation(BaseModel):
    property_id: int  # alter be UUID
    client_name: str
    client_email: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    guest_quantity: int
    active: bool # instead of deleting the reservation, we inactivate it to keep history

    model_config = {
        "from_attributes": True
    }
