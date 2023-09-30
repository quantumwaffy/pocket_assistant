from pydantic import BaseModel


class ErrorSchema(BaseModel):
    detail: str


class WebHookResponse(BaseModel):
    detail: str = "Update received"
