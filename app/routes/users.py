from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel
from typing import List
import bcrypt

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
    bytes=user.password.encode('utf-8')
    Password=bcrypt.hashpw(bytes,bcrypt.gensalt())
    new_user = User(
        name=user.name,
        role=user.role,
        password=user.password,
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
@router.get("/users/{user_name}", response_model=UserResponse)
def get_user(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/login", response_model=dict)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password==db_user.password:  # Pass user.password directly
        db_user.status = "Online"
        db.commit()
        return {"user": user.username, "details": "logged in successfully","status":1}
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
