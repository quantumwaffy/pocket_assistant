from fastapi import FastAPI, status

import routing
from config import CONFIG
from core import schemas as core_schemas
from meta import ProjectMeta


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
