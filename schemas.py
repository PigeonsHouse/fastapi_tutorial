from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class SignUpPayload(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignInPayload(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    password_hash: str

    model_config = ConfigDict(from_attributes=True)


class ReturnToken(BaseModel):
    token: str


class ContentPayload(BaseModel):
    content: str


class ContentSchema(BaseModel):
    id: str
    content: str
    user: UserSchema
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
