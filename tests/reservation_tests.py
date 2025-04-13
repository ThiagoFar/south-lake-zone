from datetime import datetime, timedelta
import pytest
from httpx import ASGITransport, AsyncClient
from starlette import status

from main import app

BASE_RESERVATION = {
    "property_id": 2,
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "guest_quantity": 2,
    "active": True
}


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to South lake zone API"}

@pytest.mark.asyncio
async def test_end_date_before_start_date():
    start_date = datetime.now()
    end_date = start_date - timedelta(days=1)
    payload = {
        **BASE_RESERVATION,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/reservation/", json=payload)




    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "end date precedes start date" in response.text.lower()