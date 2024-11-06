from pydantic import BaseModel
from typing import Optional

class AnimalSchema(BaseModel):
    tag_id: str
    animal_type: str
    photos: str
    available: bool

    class Config:
        orm_mode = True

class ApplicationSchema(BaseModel):
    adopter_name: str
    occupation: str
    animal_id: int
    status: Optional[str] = 'Pending'

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    name: str
    role: str

    class Config:
        orm_mode = True

class AppealSchema(BaseModel):
    content: str
    status: Optional[str] = 'Open'

    class Config:
        orm_mode = True
