
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=30)
    company: str = Field(min_length=2, max_length=150)
    source: str = Field(min_length=2, max_length=50)
    status: str = "New"


class LeadUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=30)
    company: str = Field(min_length=2, max_length=150)
    source: str = Field(min_length=2, max_length=50)
    status: str


class LeadResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    company: str
    source: str
    status: str

    model_config = ConfigDict(from_attributes=True)
