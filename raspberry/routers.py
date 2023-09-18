from fastapi import APIRouter, WebSocket

from logger import logger

from . import schemas

raspberry_router: APIRouter = APIRouter(
    prefix="/rasp-pi",
    tags=["Raspberry PI"],
)


@raspberry_router.websocket("/ws/sensor-data-receiver")
async def sensor_data_receiver(ws: WebSocket):
    await ws.accept()
    async for item in ws.iter_json():
        data: schemas.SensorData = schemas.SensorData(**item)
        logger.info(data)
