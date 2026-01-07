from pydantic_settings import BaseSettings, SettingsConfigDict



ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


class BaseModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')



class Settings(BaseModelSettings):
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

    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int

    @property
    def MONGO_URL(self):
        return f'mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/'
    
    REDIS_HOST: str
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/'

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
        return f'db+postgresql://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}'

broker_settings = BrokerSettings()

