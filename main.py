import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from db_schema import Book as SchemaBook
from db_schema import Author as SchemaAuthor

from db_schema import Property as SchemaProperty
from db_schema import Reservation as SchemaReservation

from db_models import Property as ModelProperty
from db_models import Reservation as ModelReservation


from db_models import Book as ModelBook
from db_models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post('/property/', response_model=SchemaProperty)
async def property(property: SchemaProperty):
    db_property = ModelProperty(title = property.title, address = property.address, city = property.city, state = property.state, country = property.country, capacity = property.capacity,
                                price_per_night = property.price_per_night, active = property.active)
    db.session.add(db_property)
    db.session.commit()
    return db_property


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.get('/book/')
async def book():
    book = db.session.query(ModelBook).all()
    return book


@app.post('/author/', response_model=SchemaAuthor)
async def author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.get('/author/')
async def author():
    author = db.session.query(ModelAuthor).all()
    return author


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)