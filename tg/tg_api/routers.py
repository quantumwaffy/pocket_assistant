from typing import Any

from aiogram import types
from fastapi import APIRouter

from config import CONFIG
from tg.tg_bot import bot_instances

from . import schemas

tg_api_router: APIRouter = APIRouter(
    prefix="/tg",
    tags=["Telegram API Management"],
)


@tg_api_router.post(CONFIG.BOT.webhook_path)
async def webhook(update: dict[str, Any]) -> schemas.WebHookResponse:
    tg_update: types.Update = types.Update(**update)
    await bot_instances.dp.feed_update(bot=bot_instances.bot, update=tg_update)
    return schemas.WebHookResponse()
