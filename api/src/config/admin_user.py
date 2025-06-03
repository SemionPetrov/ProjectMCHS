from pydantic_settings import BaseSettings
from config.env_handlels import getenvvar

class AdminUserCredentials(BaseSettings):
    ADMIN_USERNAME: str = getenvvar("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = getenvvar("ADMIN_PASSWORD")
    ADMIN_PRIVILEGE_NAME: str = getenvvar("ADMIN_PRIVILEGE_NAME")


admin_user_credentials= AdminUserCredentials()
