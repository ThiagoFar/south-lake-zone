# South Lake Zone



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ThiagoFar">
    <img src="https://bitbucket.org/midnight_raft/south-lake-zone/src/5145d4797f6cd44c2c81add6ec38548a0a4aad85/logo.png." alt="Logo" width="80" height="80">
  </a>
</div>

This is a simple API that allows for homestay reservations. it was request as a code challenge.


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Pycharm or other IDE
Create postgres Database and update .env with connection info


### Installation



1. use pip install -r /path/to/requirements.txt to get all requirements.
2. use 'alembic revision --autogenerate -m "New Migration' on terminal to create a migration.
3. use 'alembic upgrade head' to generate tha migration tables on the database.
4. use 'uvicorn main:app --reload' on terminal to start the app.
5. access http://127.0.0.1:8000/docs to check out the swagger.
   





<!-- USAGE EXAMPLES -->
## Usage

Check availability endpoint (payload):

GET
/properties/availability?property_id=1&start_date=2024-12-20&end_date=202
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

- [ ] Create property endpoint
- [ ] List property endpoint
    - [ ] filter by address, city, state, capacity and max price
- [ ] Create reservation endpoint
    - [ ] Validate property capacity x guests number
    - [ ] Validate dates (optional)
- [ ] Cancel reservation endpoint
- [ ] Check availability endpoint

Extras:

- [ ] Include unity tests
- [ ] Commands Design Pattern
- [ ] Flake8 and Black for linting and formatting
- [ ] UUID identifiers 
- [ ] Commands Design Pattern
- [ ] 'active' field to track history
- [ ] Create/Update fields included for debugging/operational
- [ ] Services for code reusability




