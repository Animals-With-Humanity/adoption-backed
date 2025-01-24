from pydantic import BaseModel
from typing import Optional

class Login(BaseModel):
    username:str
    password:str
