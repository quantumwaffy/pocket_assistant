from pydantic import BaseModel

from . import consts


class RunnerData(BaseModel):
    handler: str
    action: consts.TaskAction
