"""配置文件
"""
from pydantic import BaseSettings, Extra
from slowapi import Limiter
from slowapi.util import get_remote_address


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHMS: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_IN: int = 30  # 3 0 minutes
    REFRESH_TOKEN_EXPIRE_IN: int = 60 * 24 * 7  # 7 days
    # Redis
    REDIS_URL: str

    class Config:
        env_file = '.env'
        extra = Extra.ignore


settings = Settings()
# emailConfig = EmailConfig()
limiter = Limiter(key_func=get_remote_address)
