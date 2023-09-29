from aiogram import Bot, Dispatcher

from config import CONFIG

from . import routing

bot: Bot = Bot(token=CONFIG.BOT.TG_TOKEN, parse_mode=CONFIG.BOT.TG_PARSE_MODE)


def _init_dp() -> Dispatcher:
    dp_instance: Dispatcher = Dispatcher()
    [dp_instance.include_router(router) for router in routing.routers]
    return dp_instance


dp: Dispatcher = _init_dp()

# if __name__ == "__main__":
#     asyncio.run(dp.start_polling(bot))
