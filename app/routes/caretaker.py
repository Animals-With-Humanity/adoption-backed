from fastapi import APIRouter, Depends, HTTPException,Form,File,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Caretaker,Animal
from typing import List
from utils import caretaker_upload,signeture_upload,genrate_auth_token
from app.schemas import Login
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_KEY=os.getenv("AUTH_KEY_GEN",None)
# Create the FastAPI router
router = APIRouter()

@router.post("/caretaker/", response_model=dict)
def create_caretaker(caretaker: str = Form(...),contact: str = Form(...),whatsapp: str=Form(...),
                  address:str=Form(...),social: str=Form(...),occupation: str=Form(...),
                  username: str=Form(...),password: str=Form(...),
                  caretaker_image: UploadFile=File(...) ,
                  db: Session = Depends(get_db)):
    
    caretaker_image_address= caretaker_upload(caretaker_image)
    caretakers = db.query(Caretaker).all()
    usernames=[caretaker.caretaker_username for caretaker in caretakers]
    if username in usernames:
        raise HTTPException(status_code=404, detail="CARETAKER EXISTS: Please choose a diffrent (unique) username")
    db_caretaker = Caretaker(name=caretaker,
        contact=contact,
        caretaker_whatsapp=whatsapp,
        caretaker_add=address,
        caretaker_social=social,
        caretaker_occ=occupation,
        caretaker_username=username,
        caretaker_pass=password,
        caretaker_image=caretaker_image_address
    )
    db.add(db_caretaker)
    db.commit()
    #db.refresh(db_animal)
    return {"message": "Caretaker account created successfully","id":db_caretaker.id}
@router.get("/caretaker/", response_model=List[dict])
def get_all_caretakers(db: Session = Depends(get_db)):
    caretakers = db.query(Caretaker).all()
    return [{"id": caretaker.id,
    "Caretaker": caretaker.name,
    "Contact":caretaker.contact,
    "Whatsapp":caretaker.caretaker_whatsapp,
    "username":caretaker.caretaker_username,
    "password": caretaker.caretaker_pass,
    "signeture":caretaker.caretaker_signeture,
    "approved":caretaker.approved,
    "registered_animals":caretaker.no_animals} for caretaker in caretakers]

@router.post("/sign",response_model=dict)
def sign_form(id: int=Form(...),sign: UploadFile = File(...),db: Session = Depends(get_db)):
    db_caretaker=db.query(Caretaker).filter(Caretaker.id==id).first()
    if not db_caretaker:
        raise HTTPException(status_code=404, detail="CARETAKER NOT FOUND")
    sign_url=signeture_upload(sign)
    db_caretaker.caretaker_signeture=sign_url
    db.commit()
    return {"Success":1}


@router.put("/approve",response_model=dict)
def approve_caretaker(id:int,db: Session = Depends(get_db)):
    db_caretaker=db.query(Caretaker).filter(Caretaker.id==id).first()
    if not db_caretaker:
        raise HTTPException(status_code=404, detail="CARETAKER NOT FOUND")
    db_caretaker.approved="Approved"
    db.commit()
    return {"Success":1}

@router.put("/blacklist",response_model=dict)
def approve_caretaker(id:int,db: Session = Depends(get_db)):
    db_caretaker=db.query(Caretaker).filter(Caretaker.id==id).first()
    if not db_caretaker:
        raise HTTPException(status_code=404, detail="CARETAKER NOT FOUND")
    db_caretaker.approved="BlackListed"
    db.commit()
    return {"Success":1}

@router.get("/caretaker/{id}", response_model=dict)
def get_caretaker(id: int, db: Session = Depends(get_db)):
    caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    db_animal=db.query(Animal).filter(Animal.caretaker_id==id).all()
    if not caretaker:
        raise HTTPException(status_code=404, detail="Caretaker not found")
    return {
        "id": caretaker.id,
        "name": caretaker.name,
        "contact": caretaker.contact,
        "caretaker_whatsapp": caretaker.caretaker_whatsapp,
        "caretaker_add": caretaker.caretaker_add,
        "caretaker_social": caretaker.caretaker_social,
        "caretaker_occ": caretaker.caretaker_occ,
        "caretaker_username": caretaker.caretaker_username,
        "caretaker_password":caretaker.caretaker_pass,
        "caretaker_image": caretaker.caretaker_image,
        "signeture":caretaker.caretaker_signeture,
        "approved":caretaker.approved,
        "status":caretaker.status,
        "number_of_reg":caretaker.no_animals,
        "auth_token":caretaker.auth_token,
        "animals":[{"tag_id":animal.tag_id,"photos":animal.photos,"status":animal.avaliable} for animal in db_animal]
    }
@router.put("/login", response_model=dict)
def caretaker_login(user: Login, db: Session = Depends(get_db)):
    db_caretaker = db.query(Caretaker).filter(Caretaker.caretaker_username == user.username).first()
    if not db_caretaker:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password==db_caretaker.caretaker_pass:  # Pass user.password directly
        db_caretaker.status = "Online"
        db_caretaker.auth_token=genrate_auth_token(AUTH_KEY)
        db.commit()
        return {"user": user.username,"id":db_caretaker.id,"auth_token":db_caretaker.auth_token, "details": "logged in successfully","status":1}
    # db.refresh(dser)
    return {"details": "login failed check password"}

@router.put("/logout", response_model=dict)
def caretaker_logout(id:int, db: Session = Depends(get_db)):
    db_caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    if not db_caretaker:
        raise HTTPException(status_code=404, detail="User not found")
    db_caretaker.status="Offline"
    db_caretaker.auth_token="NULL"
    db.commit()
    return {"id":id,"details":"loged out sucessfully"}