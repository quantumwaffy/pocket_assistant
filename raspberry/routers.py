from fastapi import APIRouter, WebSocket

from config import CONFIG
from core.broadcasting import broadcast
from logger import logger

from . import models

raspberry_router: APIRouter = APIRouter(
    prefix="/rasp-pi",
    tags=["Raspberry PI"],
)


@raspberry_router.websocket("/ws/sensor-data-receiver")
async def sensor_data_receiver(ws: WebSocket):
    await ws.accept()
    async for item in ws.iter_json():
        sensor_data: models.SensorData = models.SensorData(**item)
        await sensor_data.insert()
        logger.info(sensor_data)


@raspberry_router.websocket("/ws/sensor-data-sender")
async def sensor_data_sender(ws: WebSocket):
    await ws.accept()

    async with broadcast.subscribe(CONFIG.APP.SENDER_CHANNEL) as subscriber:
        async for event in subscriber:
            logger.info(event)
            await ws.send_text(event.message)


# TODO - REMOVE AFTER TEST
@raspberry_router.get("/test/{msg}")
async def test(msg: str) -> str:
    await broadcast.publish(CONFIG.APP.SENDER_CHANNEL, msg)
    return msg
