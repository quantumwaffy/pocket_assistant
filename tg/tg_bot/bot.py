from aiogram import Bot

from config import CONFIG

bot: Bot = Bot(token=CONFIG.BOT.TG_TOKEN, parse_mode=CONFIG.BOT.TG_PARSE_MODE)
