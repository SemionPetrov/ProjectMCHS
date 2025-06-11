from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    username: str
    password: str


class UserPrivilegesResponse(BaseModel):
    privileges: List[str]


class UserModel(BaseModel):
    employee_id: int
    login: str
    password_hash: str


class EmployeeModel(BaseModel):
    last_name: str
    first_name: str
    surname: str
    birthday: str
    position_id: int 
    rang_id: int
    comment: str
