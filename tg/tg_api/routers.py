from fastapi import APIRouter

tg_api_router: APIRouter = APIRouter(
    prefix="/tg",
    tags=["Telegram API Management"],
)
