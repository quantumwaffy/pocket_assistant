from pydantic import BaseModel

from . import consts


class RunnerData(BaseModel):
    task: str
    action: consts.TaskAction
