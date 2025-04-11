from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship('Author')


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Property(Base):
    __tablename__ = 'property'
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    capacity = Column(Integer)
    price_per_night = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean)

class Reservation(Base):
    __tablename__ = 'reservation'
    id  = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('property.id'))
    client_name = Column(String)
    client_email = Column(String)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    guest_quantity = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean)

    property = relationship('Property')

