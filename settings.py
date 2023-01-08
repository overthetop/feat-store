from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_hostname: str = Field(..., env='DATABASE_HOSTNAME')
    database_port: str = Field(..., env='DATABASE_PORT')
    database_username: str = Field(..., env='DATABASE_USERNAME')
    database_password: str = Field(..., env='DATABASE_PASSWORD')
    database_name: str = Field(..., env='DATABASE_NAME')


settings = Settings()
