from fastapi import APIRouter, WebSocket

from config import CONFIG
from core.broadcasting import broadcast
from logger import logger

from . import consts, models, schemas

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
@raspberry_router.get("/test-led/{state}")
async def test_led(state: consts.TaskAction) -> str:
    msg = schemas.RunnerData(task="LEDSocketTask", action=state)
    await broadcast.publish(CONFIG.APP.SENDER_CHANNEL, msg.model_dump_json())
    return "OK"


# TODO - REMOVE AFTER TEST
@raspberry_router.get("/test-buzzer/{state}")
async def test_buzzer(state: consts.TaskAction) -> str:
    msg = schemas.RunnerData(task="BuzzerTask", action=state)
    await broadcast.publish(CONFIG.APP.SENDER_CHANNEL, msg.model_dump_json())
    return "OK"
