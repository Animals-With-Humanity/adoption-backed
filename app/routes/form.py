from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Request,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application,GenralInfo
from pydantic import BaseModel
from typing import List
from app.models import Animal
from handel_file import adoptor_upload
# Create the FastAPI router
class GenralInfoSchema(BaseModel):
    plans: str
    pets : str
    alone: str
    temp_caretaker: str

router = APIRouter()
@router.post("/approve",response_model=dict)
def Approve_request(application_id: int,info:GenralInfoSchema, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    info=GenralInfo(
        tag_id=db_application.tag_id,
        application_id=db_application.id,
        plans=info.plans,
        pets=info.pets,
        alone=info.alone,
        temp_caretaker=info.temp_caretaker
    )
    db.add(info)
    db_application.status="Approved"
    db.commit() 
    return {"Success":1}
@router.post("/decline",response_model=dict)
def Decline_request(application_id: int,info:GenralInfoSchema, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db_application.status="Decline"
    db.commit() 
    return {"Success":1}
@router.get("/form",response_model=dict)
def get_form(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    animal = db.query(Animal).filter(Animal.tag_id == application.tag_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    info = db.query(GenralInfo).filter(GenralInfo.application_id == application_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"meta":{
            "id": application.id,
            "tag_id":animal.tag_id
            },
            "Animal":{
            "age":animal.age,
            "type":animal.animal_type,
            "gender":animal.gender,
            "fitness":animal.fitness,
            "sterilisation":animal.sterilisation,
            "vaccination":animal.vaccination,
            "photos":animal.photos
            },
            "Caretaker":{
            "caretaker":animal.caretaker,
            "contact":animal.contact,
            "whatsapp":animal.caretaker_whatsapp,
            "address":animal.caretaker_add,
            "social":animal.caretaker_social,
            "occupation":animal.caretaker_occ,
            "caretaker_image":animal.caretaker_image,
            "caretaker_doc":animal.caretaker_doc
            },
            "Adoptor":{
            "name": application.adopter_name,
            "occupation": application.occupation,
            "contact": application.contact,
            "whatsapp": application.whatsapp,
            "address": application.Address, 
            "home_type": application.homeType,  
            "adopter_image": application.adopter_image,  
            "adopter_doc": application.adopter_doc
            },
            "Genral Information":{
                "plans":info.plans,
                "pets":info.pets,
                "alone":info.alone,
                "temp_caretaker":info.temp_caretaker
            }
            }