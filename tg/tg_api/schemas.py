from pydantic import BaseModel


class WebHookResponse(BaseModel):
    detail: str = "Update received"
