from pydantic import BaseModel, EmailStr


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
