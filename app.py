import asyncio

from beanie import init_beanie
from fastapi import FastAPI, status

import routing
from config import CONFIG
from core import broadcasting
from core import schemas as core_schemas
from meta import ProjectMeta
from raspberry import models as rasp_models
from tg.tg_bot import bot_instances


def get_app() -> FastAPI:
    """Initializes and returns a FastAPI object"""
    project_meta: ProjectMeta = ProjectMeta()
    api: FastAPI = FastAPI(
        debug=CONFIG.APP.DEBUG,
        swagger_ui_parameters={"persistAuthorization": True},
        title=project_meta.title,
        description=project_meta.description,
        responses={status.HTTP_403_FORBIDDEN: {"model": core_schemas.ErrorSchema}},
        version=project_meta.version,
        **{"docs_url": None, "redoc_url": None} if not CONFIG.APP.DEBUG else {},
    )
    for prefix, routs in routing.AppRouter.routers:
        [api.include_router(router, prefix=prefix) for router in routs]
    return api


app: FastAPI = get_app()


@app.on_event("startup")
async def startup() -> None:
    await broadcasting.broadcast.connect()
    await init_beanie(
        database=CONFIG.MONGO.client[CONFIG.MONGO.MONGO_INITDB_DATABASE],
        document_models=[rasp_models.SensorData],
    )
    asyncio.create_task(bot_instances.dp.start_polling(bot_instances.bot))  # TODO: REMOVE POOLING AFTER TEST


@app.on_event("shutdown")
async def shutdown() -> None:
    await broadcasting.broadcast.disconnect()
