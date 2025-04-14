# South Lake Zone



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ThiagoFar">
    <img src="logo.png" alt="Logo" width="400" height="400">
  </a>
</div>




<!-- GETTING STARTED -->
## Getting Started
This is a simple API that allows for homestay reservations. it was requested as a code challenge.
project link : https://github.com/ThiagoFar/south-lake-zone

### Prerequisites

Pycharm or other IDE
Create postgres Database and update .env with connection info


### Installation



1. use pip install -r /path/to/requirements.txt to get all requirements.
2. create a .env file in the root of the project and fill it with the database info, example: ```DATABASE_URL = 'postgresql://postgres:<PASSWORD>@localhost/<DATABASE>```
3. Use ```alembic revision --autogenerate -m "New Migration" ``` on terminal to create a migration.
4. Use ```alembic upgrade head``` to generate tha migration tables on the database.
5. Use ```uvicorn main:app --reload``` on terminal to start the app.
6. Access http://127.0.0.1:8000/docs to check out the swagger.
   


<!-- USAGE EXAMPLES -->
## Usage

Check availability endpoint (payload):

REQUEST: 

GET /properties/availability?property_id=1&start_date=2024-12-20&end_date=202
4-12-27&guests_quantity=4

RESPONSE: 

{
  "stay_duration": 5,
  "available": false,
  "message": "The date is already booked."
}


<!-- ROADMAP -->
## Roadmap

Requested functionality: 

- [X] Create property endpoint
- [X] List property endpoint
    - [X] filter by address, city, state, capacity and max price
- [X] Create reservation endpoint
    - [X] Validate property capacity x guests number
    - [X] Validate dates (optional)
- [X] Cancel reservation endpoint
- [X] Check availability endpoint

Extras:

- [X] Include unity tests
- [X] Commands Design Pattern
- [X] S.O.L.I.D and pythonic adherence
- [X] Flake8 and Black for linting and formatting
- [ ] UUID identifiers
- [X] 'active' field to track history
- [X] Create/Update fields included for debugging/operational
- [X] HTTP ERROR CODES




