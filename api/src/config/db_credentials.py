from pydantic_settings import BaseSettings
from config.env_handlels import getenvvar

"""
Handles db info given by env vars
import settings to get them.
Used by main to create db connection.
"""

class Settings(BaseSettings):
    DB_HOST: str = getenvvar("DATABASE_HOST")
    DB_USER: str = getenvvar("DATABASE_USERNAME") 
    DB_PASSWORD: str = getenvvar("DATABASE_PASSWORD") 
    DB_PORT: int = int(getenvvar("DATABASE_PORT"))
    DB_NAME: str = getenvvar("DATABASE") 

settings = Settings()
