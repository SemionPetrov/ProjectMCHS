from pydantic_settings import BaseSettings
from config.env_handlels import getenvvar

"""
Handles admin credentials given by env vars
import admin_user_credentials to get them.
Used by db fixtues.
"""

class AdminUserCredentials(BaseSettings):
    ADMIN_USERNAME: str = getenvvar("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = getenvvar("ADMIN_PASSWORD")
    ADMIN_PRIVILEGE_NAME: str = getenvvar("ADMIN_PRIVILEGE_NAME")


admin_user_credentials= AdminUserCredentials()
