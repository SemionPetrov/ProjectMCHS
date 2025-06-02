from pydantic_settings import BaseSettings

"""DO NOT SHARE OR COMMIT IN PROD"""

class Settings(BaseSettings):
    DB_HOST: str = "mysql"
    DB_USER: str = "root"
    DB_PASSWORD: str = "pwd123admin"
    DB_PORT: int = 3306
    DB_NAME: str = "projectmchs_db"

settings = Settings()
