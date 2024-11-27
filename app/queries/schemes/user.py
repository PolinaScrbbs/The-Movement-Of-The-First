from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    full_name: str
