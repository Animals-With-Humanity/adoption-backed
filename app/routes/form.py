from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Request,Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application,Lead,Caretaker
from pydantic import BaseModel
from typing import List
from app.models import Animal
from utils import signeture_upload

# Create the FastAPI router
class GenralInfoSchema(BaseModel):
    councler_name:str
    plans: str
    pets : str
    alone: str
    temp_caretaker: str

class DummyData:
    councler_name="NA"
    plans="NA"
    pets=False      
    alone="NA"
    temp_caretaker="NA"
    adoptor_signeture="NA"
    caretaker_signeture="NA"

router = APIRouter()
@router.post("/approve",response_model=dict)
def Approve_request(application_id: int,info:GenralInfoSchema, db: Session = Depends(get_db)):
    db_application = db.query(Lead).filter(Lead.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    info=Application(
        tag_id=db_application.tag_id,
        application_id=db_application.id,
        councler_name=info.councler_name,
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
def Decline_request(application_id: int, db: Session = Depends(get_db)):
    db_application = db.query(Lead).filter(Lead.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    animal = db.query(Animal).filter(Animal.tag_id == db_application.tag_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db_application.status="Denied"
    animal.avaliable=True
    db.commit() 
    return {"Success":1}
@router.post("/cancle",response_model=dict)
def Cancle_request(application_id: int,remarks:str, db: Session = Depends(get_db)):
    db_application = db.query(Lead).filter(Lead.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    animal = db.query(Animal).filter(Animal.tag_id == db_application.tag_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db_application.status="Cancled"
    db_application.remarks=remarks
    animal.avaliable=True
    db.commit() 
    return {"Success":1}
@router.get("/form",response_model=dict)
def get_form(application_id: int, db: Session = Depends(get_db)):
    db_lead=db.query(Lead).filter(Lead.id==application_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Application not found")
    if db_lead.status =="Pending" or db_lead.status =="Approved" or db_lead.status =="Cancled":
        db_application=db.query(Application).filter(Application.application_id==application_id).first()
        if not db_application:
            raise HTTPException(status_code=404, detail="Application has not been forwarded by the PAC team")
    else:
        db_application=DummyData()
    db_animal=db.query(Animal).filter(Animal.tag_id==db_lead.tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal details not found")
    db_caretaker=db.query(Caretaker).filter(Caretaker.id==db_animal.caretaker_id).first()

    if db_lead.status == "Cancled":
        return {"meta":{
            "id": db_lead.id,
            "tag_id":db_animal.tag_id
            },
            "Animal":{
            "age":db_animal.age,
            "type":db_animal.animal_type,
            "gender":db_animal.gender,
            "fitness":db_animal.fitness,
            "sterilisation":db_animal.sterilisation,
            "vaccination":db_animal.vaccination,
            "photos":db_animal.photos
            },
            "Caretaker":{
            "caretaker":db_caretaker.name,
            "contact":db_caretaker.contact,
            "whatsapp":db_caretaker.caretaker_whatsapp,
            "address":db_caretaker.caretaker_add,
            "social":db_caretaker.caretaker_social,
            "occupation":db_caretaker.caretaker_occ,
            "caretaker_image":db_caretaker.caretaker_image,
            },
            "Adoptor":{
            "name": db_lead.adopter_name,
            "occupation": db_lead.occupation,
            "contact": db_lead.contact,
            "whatsapp": db_lead.whatsapp,
            "address": db_lead.Address, 
            "address_permanent":db_lead.Address_permanent,
            "home_type": db_lead.homeType,
            "social":db_lead.social,  
            "adopter_image": db_lead.adopter_image,  
            "adopter_doc_front": db_lead.adopter_doc_front,
            "adopter_doc_back": db_lead.adopter_doc_back,
            "status":db_lead.status,
            "remarks":db_lead.remarks
            },
            "GenralInformation":{
                "councler":db_application.councler_name,
                "plans":db_application.plans,
                "pets":db_application.pets,
                "alone":db_application.alone,
                "temp_caretaker":db_application.temp_caretaker,
                "adoptor_signeture":db_application.adoptor_signeture,
                "caretaker_signeture":db_caretaker.caretaker_signeture
            }
            }
    return {"meta":{
            "id": db_lead.id,
            "tag_id":db_animal.tag_id
            },
            "Animal":{
            "age":db_animal.age,
            "type":db_animal.animal_type,
            "gender":db_animal.gender,
            "fitness":db_animal.fitness,
            "sterilisation":db_animal.sterilisation,
            "vaccination":db_animal.vaccination,
            "photos":db_animal.photos
            },
            "Caretaker":{
            "caretaker":db_caretaker.name,
            "contact":db_caretaker.contact,
            "whatsapp":db_caretaker.caretaker_whatsapp,
            "address":db_caretaker.caretaker_add,
            "social":db_caretaker.caretaker_social,
            "occupation":db_caretaker.caretaker_occ,
            "caretaker_image":db_caretaker.caretaker_image,
            },
            "Adoptor":{
            "name": db_lead.adopter_name,
            "occupation": db_lead.occupation,
            "contact": db_lead.contact,
            "whatsapp": db_lead.whatsapp,
            "address": db_lead.Address,
            "address_permanent":db_lead.Address_permanent,
            "home_type": db_lead.homeType,
            "social":db_lead.social,  
            "adopter_image": db_lead.adopter_image,  
            "adopter_doc_front": db_lead.adopter_doc_front,
            "adopter_doc_back": db_lead.adopter_doc_back,
            "status":db_lead.status 
            },
            "GenralInformation":{
                "councler":db_application.councler_name,
                "plans":db_application.plans,
                "pets":db_application.pets,
                "alone":db_application.alone,
                "temp_caretaker":db_application.temp_caretaker,
                "adoptor_signeture":db_application.adoptor_signeture,
                "caretaker_signeture":db_caretaker.caretaker_signeture
            }
    }

@router.post("/sign",response_model=dict)
def sign_form(application_id: int=Form(...),user: str=Form(...),sign: UploadFile = File(...),db: Session = Depends(get_db)):
    db_application=db.query(Application).filter(Application.application_id==application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application has not been forwarded by the PAC team")
    sign_url=signeture_upload(sign)
    if user=='adoptor':
        db_application.adoptor_signeture=sign_url
    else:
        raise HTTPException(status_code=404, detail="Invalid user type please check spellings")
    db.commit()
    return {"Success":1}
