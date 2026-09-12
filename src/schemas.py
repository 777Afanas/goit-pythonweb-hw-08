from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
