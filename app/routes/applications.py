from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application
from pydantic import BaseModel
from typing import List
from app.models import Animal

# Create the FastAPI router
router = APIRouter()

# Pydantic schema for an application
class ApplicationCreate(BaseModel):
    tag_id: int
    name: str
    contact: str
    whatsapp: str
    address: str    
    occupation: str
    pets: bool
    hometype: str
class ApplicationUpdate(BaseModel):
    status:str

# Route to create a new application
@router.post("/applications/", response_model=dict)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    db_application = Application(
        adopter_name=application.name,
        occupation=application.occupation,
        tag_id=application.tag_id)
    db.add(db_application)
    #db.commit()
    db_animal = db.query(Animal).filter(Animal.tag_id == application.tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found") 
    db_animal.available=False
    db.commit()

    #db.refresh(db_application)
    return {"message": "Application created successfully", "application_id": db_application.id}

# Route to get all applications
@router.get("/applications/", response_model=List[dict])
def get_all_applications(db: Session = Depends(get_db)):
    applications = db.query(Application).all()
    return [{"id": app.id, "name": app.adopter_name, "occupation": app.occupation, "tag_id": app.tag_id,"status":app.status} for app in applications]

# Route to get a single application by ID
@router.get("/applications/{application_id}", response_model=dict)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"id": application.id, "name": application.adopter_name, "occupation": application.occupation, "animal_id": application.tag_id}

# Route to update an application
@router.put("/applications/{tag_id}", response_model=dict)
def update_application(tag_id: int,id:int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.tag_id == tag_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db_application.status = application.status
    db.commit()
    #db.refresh(db_application)
    return {"message": "Application updated successfully", "application_id": db_application.id}

# Route to delete an application
@router.delete("/applications/{application_id}", response_model=dict)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"message": "Application deleted successfully"}
