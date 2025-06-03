from pydantic_settings import BaseSettings
from os import getenv


class EnvVarNotFound(Exception): 
    def __init__(self, variable):
        self.variable = variable

    def __str__(self) -> str:
        return f"Could not find {self.variable} in env!\nCheck local.env!"


def getenvvar(var_name: str):
    var = getenv(var_name)
    if var == None:
        raise EnvVarNotFound(var_name)
    return var



class Settings(BaseSettings):
    DB_HOST: str = getenvvar("DATABASE_HOST")
    DB_USER: str = getenvvar("DATABASE_USERNAME") 
    DB_PASSWORD: str = getenvvar("DATABASE_PASSWORD") 
    DB_PORT: int = int(getenvvar("DATABASE_PORT"))
    DB_NAME: str = getenvvar("DATABASE") 

settings = Settings()
