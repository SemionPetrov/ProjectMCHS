from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    username: str
    password: str

class UserPrivilegesResponse(BaseModel):
    privileges: List[str]

