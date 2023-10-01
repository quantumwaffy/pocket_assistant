import uuid

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

from core import base as core_base
from core import mixins as core_mixins


class AppConfig(core_mixins.EnvConfigMixin):
    DEBUG: bool = False
    SENDER_CHANNEL: str = uuid.uuid4().hex


class MongoConfig(core_base.ServiceConfig):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    MONGO_HOST: str
    MONGO_CONNECTION_TYPE: str = "mongodb"
    MONGO_AUTH_SOURCE: str = "admin"
    MONGO_EXTRA_URL_PARAMS: str = "retryWrites=true&w=majority"

    @property
    def url(self) -> str:
        return (
            f"{self.MONGO_CONNECTION_TYPE}://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@"
            f"{self.MONGO_HOST}/{self.MONGO_INITDB_DATABASE}?authSource={self.MONGO_AUTH_SOURCE}"
            f"&{self.MONGO_EXTRA_URL_PARAMS}"
        )

    @property
    def client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(self.url)


class RedisConfig(core_base.ServiceConfig):
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class TelegramBotConfig(core_mixins.EnvConfigMixin):
    TG_TOKEN: str
    TG_WEBHOOK_PROXY_NGROK_DOMAIN: str
    TG_PARSE_MODE: str = "HTML"

    @property
    def webhook_path(self) -> str:
        return "/webhook"

    @property
    def webhook_url(self) -> str:
        return f"https://{self.TG_WEBHOOK_PROXY_NGROK_DOMAIN}{self.webhook_path}"


class Config(BaseSettings):
    """Project settings"""

    APP: AppConfig = AppConfig()
    MONGO: MongoConfig = MongoConfig()
    REDIS: RedisConfig = RedisConfig()
    BOT: TelegramBotConfig = TelegramBotConfig()


CONFIG: Config = Config()
