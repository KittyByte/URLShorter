from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


class BaseModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class Settings(BaseModelSettings):
    BOT_TOKEN: str = Field(validation_alias='TELEGRAM_BOT_TOKEN')
    SECRET_KEY: str

settings = Settings()


class DBSettings(BaseModelSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    MONGO_URL: str

db_settings = DBSettings()


class BrokerSettings(BaseModelSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_VHOST: str

    @property
    def CELERY_BROKER_URL(self):
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}'
    @property
    def CELERY_RESULT_BACKEND(self):
        return f'db+postgresql://\
            {db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}'

broker_settings = BrokerSettings()

