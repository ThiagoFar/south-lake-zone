# build a schema using pydantic
import datetime
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True

class Author(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

class Property(BaseModel):
    title: str
    address: str
    city: str
    state: str
    country: str
    capacity: int
    price_per_night: int
    active: bool

    class Config:
        orm_mode = True

class Reservation(BaseModel):
    property_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    guest_quantity: int
    active: bool

    class Config:
        orm_mode = True
