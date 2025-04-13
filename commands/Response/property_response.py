from pydantic import BaseModel


class AvailabilityResponse(BaseModel):
    stay_duration: int
    available: bool
    message: str