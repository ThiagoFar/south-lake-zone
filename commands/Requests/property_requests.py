from pydantic import BaseModel
import datetime

class avaliability_request(BaseModel):
    property_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    guest_quantity: int
