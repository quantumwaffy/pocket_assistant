import datetime

from pydantic import BaseModel, Field


class SensorData(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    sound: int | None = None
    light: int | None = None
    timestamp: int = Field(default_factory=lambda: datetime.datetime.now().timestamp())
