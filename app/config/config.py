from pydantic_settings import BaseSettings
#references https://docs.pydantic.dev/2.1/api/pydantic_settings/?utm_source=chatgpt.com
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()