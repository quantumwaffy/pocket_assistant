import itertools

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import User
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from beanie.odm.enums import SortDirection

from config import CONFIG
from core.broadcasting import broadcast
from raspberry import consts as rasp_consts
from raspberry import models as rasp_models
from raspberry import schemas as rasp_schemas

from . import consts

base_router: Router = Router()

routers: tuple[Router, ...] = (base_router,)


@base_router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    user_attrs: tuple[str, ...] = ("id", "first_name", "last_name", "username")
    user: User = message.from_user
    user_data: str = " | ".join(str(value) for attr in user_attrs if (value := getattr(user, attr)))
    await message.answer(f"Hi there, {user_data}")


@base_router.message(Command("pi"))
async def raspberry_handler(message: types.Message) -> None:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    for task, action in itertools.product(rasp_consts.Task.names, rasp_consts.TaskAction.names):
        kb_builder.add(types.KeyboardButton(text=f"{consts.PI_BUTTON_TASK_PREFIX}_{task}_{action}"))
    kb_builder.add(types.KeyboardButton(text=f"{consts.PI_BUTTON_TASK_PREFIX}_{consts.PI_BUTTON_LAST_SENSORS_DATA}"))
    kb_builder.adjust(2)
    await message.answer("Select the PI option", reply_markup=kb_builder.as_markup(resize_keyboard=True))


@base_router.message(F.text.startswith(consts.PI_BUTTON_TASK_PREFIX))
async def led_on(message: types.Message) -> None:
    msg_text: str = message.text
    if consts.PI_BUTTON_LAST_SENSORS_DATA in msg_text:
        last_data: rasp_models.SensorData | None = (
            await rasp_models.SensorData.find().sort(("timestamp", SortDirection.DESCENDING)).limit(1).first_or_none()
        )
        if last_data:
            units: dict[str, str] = rasp_consts.SensorMeasurementUnit.name_value
            answer: str = ""
            for _type, value in last_data.model_dump(exclude={"timestamp", "id"}).items():
                value_text: str = (
                    f"{value} {units.get(_type, '')}" if value is not None else consts.PI_BUTTON_SENSORS_ITEM_EMPTY
                )
                answer += f"{_type.capitalize()} - {value_text}\n"
            await message.answer(answer.strip("\n"))
        else:
            await message.answer(consts.PI_BUTTON_NO_LAST_SENSORS_DATA)
    else:
        _, task_name, action_name = msg_text.split("_")
        task_value: str = rasp_consts.Task.name_value[task_name]
        action_value: str = rasp_consts.TaskAction.name_value[action_name]
        data: rasp_schemas.RunnerData = rasp_schemas.RunnerData(task=task_value, action=action_value)
        await broadcast.publish(CONFIG.APP.SENDER_CHANNEL, data.model_dump_json())
        await message.answer(f"{msg_text}: {consts.PI_TASK_APPLIED_PART_MSG}")
