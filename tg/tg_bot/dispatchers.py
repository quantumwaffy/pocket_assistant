from aiogram import Dispatcher

from . import routing


def _init_dp() -> Dispatcher:
    dp_instance: Dispatcher = Dispatcher()
    [dp_instance.include_router(router) for router in routing.routers]
    return dp_instance


base_dp: Dispatcher = _init_dp()
