from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from pydantic import BaseModel
from typing import List

# Create the FastAPI router
router = APIRouter()

# Pydantic schema for user data
class UserCreate(BaseModel):
    name: str
    role: str
    password: str

class UserLogin(BaseModel):
    status: str

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
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    new_user = User(
        name=user.name,
        role=user.role,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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

# Route to logi a user entry
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.status=user.status
    db.commit()
    db.refresh(db_user)
    return db_user

# Route to delete a user
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
