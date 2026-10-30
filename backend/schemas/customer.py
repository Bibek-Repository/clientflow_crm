from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: str


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    company: str