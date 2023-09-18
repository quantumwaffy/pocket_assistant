from pydantic_settings import BaseSettings

from core import mixins as core_mixins


class AppConfig(core_mixins.EnvSettingsMixin):
    DEBUG: bool = False


class Config(BaseSettings):
    """Project settings"""

    APP: AppConfig = AppConfig()


CONFIG: Config = Config()
