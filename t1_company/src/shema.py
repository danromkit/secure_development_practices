from pydantic import BaseModel, Field


class User(BaseModel):
    login: str = Field(default=None, max_length=300, title="Login")
    password: str = Field(default=None, max_length=300, title="Hashed Password")
