from pydantic import BaseModel
import datetime


class AvailabilityRequest(BaseModel):
    property_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    guest_quantity: int

class GetPropertyRequest(BaseModel):
    address: str = ""
    city: str = ""
    state: str = ""
    max_price: float = 0
