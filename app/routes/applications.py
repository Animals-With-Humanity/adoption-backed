from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Request,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application
from pydantic import BaseModel
from typing import List
from app.models import Animal
from handel_file import adoptor_upload
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
def create_application(tag_id: int = Form(...),
                       name: str = Form(...),
                       contact: str = Form(...),
                       whatsapp: str = Form(...),
                       address: str = Form(...),
                       occupation: str = Form(...),
                       pets: bool = Form(...),
                       hometype: str = Form(...),
                       adopter_image: UploadFile = File(...),
                       adopter_doc: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    img="www.example.com/sample.jpg"#adoptor_upload(adopter_image)
    doc="www.example.com/sample.jpg"#adoptor_upload(adopter_doc)
    db_application = Application(
        tag_id=tag_id,
        adopter_name=name,
        contact=contact,
        whatsapp=whatsapp,
        Address=address,
        occupation=occupation,
        pets=pets,
        homeType=hometype,
        adopter_image=img,
        adopter_doc=doc,
        status="Pending"
        )
    db.add(db_application)
    #db.commit()
    db_animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
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
    return {
    "id": application.id,
    "name": application.adopter_name,
    "occupation": application.occupation,
    "animal_id": application.tag_id,
    "contact": application.contact,
    "whatsapp": application.whatsapp,
    "address": application.Address,  
    "pets": application.pets,
    "home_type": application.homeType,  
    "adopter_image": application.adopter_image,  
    "adopter_doc": application.adopter_doc,
    "status": application.status}

# Route to update an application
@router.put("/applications/{tag_id}", response_model=dict)
def update_application(tag_id: int,id:int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.tag_id == tag_id).first()
    animal=db.query(Animal).filter(Animal.tag_id==tag_id).first()
    data={}
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.status == "Approved":
        data={"tag_id":animal.tag_id,
            "age":animal.age,
            "type":animal.animal_type,
            "gender":animal.gender,
            "fitness":animal.fitness,
            "sterilisation":animal.sterilisation,
            "vaccination":animal.vaccination,
            "caretaker":animal.caretaker,
            "contact":animal.contact,
            "photos":animal.photos,
            "avaliable":animal.available,
            "id": db_application.id,
            "name": db_application.adopter_name,
            "occupation": db_application.occupation,
            "animal_id": db_application.tag_id,
            "contact": db_application.contact,
            "whatsapp": db_application.whatsapp,
            "address": db_application.Address,  
            "pets": db_application.pets,
            "home_type": db_application.homeType,  
            "adopter_image": db_application.adopter_image,  
            "adopter_doc": db_application.adopter_doc,
            "status": db_application.status}
        print("create and upload form")
    elif application.status=="Denied":
        db_animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
        db_animal.available=True
    db_application.status = application.status
    db.commit()
    #db.refresh(db_application)
    return data
    #return {"message": "Application updated successfully", "application_id": db_application.id}

# Route to delete an application
@router.delete("/applications/{application_id}", response_model=dict)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"message": "Application deleted successfully"}
