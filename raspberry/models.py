import datetime

from beanie import Document
from pydantic import Field


class SensorData(Document):
    temperature: float | None = None
    humidity: float | None = None
    sound: int | None = None
    light: int | None = None
    timestamp: int = Field(default_factory=lambda: datetime.datetime.now().timestamp())
