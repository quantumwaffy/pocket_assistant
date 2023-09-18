from pydantic_settings import BaseSettings


class EnvSettingsMixin(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = None
