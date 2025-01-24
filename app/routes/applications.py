from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, Animal,Caretaker
from pydantic import BaseModel
from typing import List
from utils import adoptor_upload

# Create the FastAPI router
router = APIRouter()

# Pydantic schema for updating application status
class ApplicationUpdate(BaseModel):
    status: str

# Route to create a new application
@router.post("/applications/", response_model=dict)
def create_application(
    animal_tag_id: str = Form(...),
    name: str = Form(...),
    contact: str = Form(...),
    whatsapp: str = Form(...),
    address: str = Form(...),
    address_permanent: str=Form(...),
    house_type: str=Form(...),
    occupation: str = Form(...),
    email: str = Form(...),
    social: str = Form(...),
    adopter_image: UploadFile = File(...),
    adopter_doc_front: UploadFile = File(...),
    adopter_doc_back: UploadFile = File(...),
    incamp: str = Form(...),
    db: Session = Depends(get_db),
):
    # Upload adopter images
    img_url = adoptor_upload(adopter_image)
    front_url = adoptor_upload(adopter_doc_front)
    back_url = adoptor_upload(adopter_doc_back)
    db_animal = db.query(Animal).filter(Animal.tag_id == animal_tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db_animal.avaliable = False
    # Create a new lead entry
    db_lead = Lead(
        tag_id=animal_tag_id,
        adopter_name=name,
        contact=contact,
        whatsapp=whatsapp,
        Address=address,
        Address_permanent=address_permanent,
        occupation=occupation,
        Email=email,
        social=social,
        homeType=house_type,
        adopter_image=img_url,
        adopter_doc_front=front_url,
        adopter_doc_back=back_url,
        incamp=incamp,
        status="Pending",
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return {"message": "Application created successfully", "application_id": db_lead.id}

# Route to get all applications
@router.get("/applications/", response_model=List[dict])
def get_all_applications(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return [
        {
            "id": lead.id,
            "animal_tag_id": lead.tag_id,
            "name": lead.adopter_name,
            "contact": lead.contact,
            "whatsapp": lead.whatsapp,
            "occupation": lead.occupation,
            "status": lead.status,
        }
        for lead in leads
    ]

# Route to get a single application by ID
@router.get("/applications/{application_id}", response_model=dict)
def get_application(application_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == application_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Application not found")

    animal = db.query(Animal).filter(Animal.tag_id == lead.tag_id).first()
    caretaker=db.query(Caretaker).filter(Caretaker.id==animal.caretaker_id).first()
    return {
        "id": lead.id,
        "name": lead.adopter_name,
        "occupation": lead.occupation,
        "animal_id": lead.tag_id,
        "contact": lead.contact,
        "whatsapp": lead.whatsapp,
        "address": lead.Address,
        "address_permanent":lead.Address_permanent,
        "email": lead.Email,
        "social": lead.social,
        "adopter_image": lead.adopter_image,
        "adopter_doc_front": lead.adopter_doc_front,
        "adopter_doc_back": lead.adopter_doc_back,
        "status": lead.status,
        "remarks":lead.remarks,
        "animal_details": {
            "id": animal.id,
            "type": animal.animal_type,
            "photos": animal.photos,
            "avaliable": animal.avaliable,
        },
        "caretaker_details":{
            "id":caretaker.id,
            "name":caretaker.name,
            "Contact_number":caretaker.contact,
            "whatsapp": caretaker.caretaker_whatsapp
            }
    }

# Route to update an application
@router.put("/applications/{application_id}", response_model=dict)
def update_application( 
    application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)
):
    db_lead = db.query(Lead).filter(Lead.id == application_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Application not found")

    animal = db.query(Animal).filter(Animal.id == db_lead.animal_id).first()

    if application.status == "Approved":
        db_lead.status = "Approved"
        # Here, you can implement additional logic like generating forms or notifications.

    elif application.status == "Denied":
        db_lead.status = "Denied"
        # Make the animal avaliable again if denied.
        if animal:
            animal.avaliable = True

    elif application.status == "Cancled":
        db_lead.status = "Cancled"
        if animal:
            animal.avaliable = True

    else:
        db_lead.status = "Pending"

    db.commit()
    db.refresh(db_lead)
    return {"message": "Application updated successfully", "application_id": db_lead.id}

# Route to delete an application
@router.delete("/applications/{application_id}", response_model=dict)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == application_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_lead)
    db.commit()
    return {"message": "Application deleted successfully"}
