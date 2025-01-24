from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel
from typing import List
from utils import hash_password,verify_password,genrate_auth_token
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_KEY=os.getenv("AUTH_KEY_GEN",None)
# Create the FastAPI router
router = APIRouter()

# Pydantic schema for user data
class UserCreate(BaseModel):
    name: str
    role: str
    password: str

class UserLogin(BaseModel):
    username:str
    password:str

# Pydantic schema for user response
class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    password: str
    status: str

    class Config:
        orm_mode = True

# Route to create a new user
@router.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    password=hash_password(user.password)
    new_user = User(
        name=user.name,
        role=user.role,
        password=password,
        status='Offline'
    )
    db.add(new_user)
    db.commit()
    #db.refresh(new_user)
    return {"user":user.name,"id":new_user.id,"role":new_user.role,"status":new_user.status}

# Route to get all users
@router.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Route to get a single user by ID
@router.get("/users/{user_name}", response_model=dict)
def get_user(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status":user.status,"auth_token":user.auth_token}

@router.put("/users/login", response_model=dict)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if verify_password(user.password,db_user.password):
        db_user.status = "Online"
        db_user.auth_token=genrate_auth_token(AUTH_KEY)
        db.commit()
        return {"user": user.username,"auth_token":db_user.auth_token, "details": "logged in successfully","status":1}
    # db.refresh(dser)
    return {"details": "login failed check password"}

@router.put("/users/logout", response_model=dict)
def user_logout(user: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.status="Offline"
    db.commit()
    return {"user":user,"details":"loged out sucessfully"}
    
# Route to delete a user
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
