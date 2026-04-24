from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=255)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
