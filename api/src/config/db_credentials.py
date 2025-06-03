from pydantic_settings import BaseSettings
from config.env_handlels import getenvvar

class Settings(BaseSettings):
    DB_HOST: str = getenvvar("DATABASE_HOST")
    DB_USER: str = getenvvar("DATABASE_USERNAME") 
    DB_PASSWORD: str = getenvvar("DATABASE_PASSWORD") 
    DB_PORT: int = int(getenvvar("DATABASE_PORT"))
    DB_NAME: str = getenvvar("DATABASE") 

settings = Settings()
