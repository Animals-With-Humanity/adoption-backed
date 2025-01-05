from fastapi import APIRouter, Depends, HTTPException,Form,File,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal
from pydantic import BaseModel
from typing import List
from utils import animal_upload,caretaker_upload
# Create the FastAPI router
router = APIRouter()

# Pydantic schema for animal data
#class AnimalCreate(BaseModel):
#    tag_id: int
#    gender: str
#    fitness: str
#    vaccination: bool
#    sterilisation: bool
#    animal_type: str
#    caretaker: str
#    contact: str
#    photos: str  # Could be a URL or path to the photos

class AnimalUpdate(BaseModel):
    available:bool

# Route to create a new animal entry
@router.post("/animals/", response_model=dict)
def create_animal(tag_id: str=Form(...),gender: str=Form(...),
                  age: int = Form(...),fitness: str= Form(...),vaccination: bool=Form(...),
                  sterilisation:bool=Form(...),animal_type: str = Form(...),
                  caretaker: str = Form(...),contact: str = Form(...),whatsapp: str=Form(...),
                  address:str=Form(...),social: str=Form(...),occupation: str=Form(...),
                  animal: UploadFile=File(...) ,caretaker_image: UploadFile=File(...) ,
                  db: Session = Depends(get_db)):
    
    file_url=animal_upload(animal)
    caretaker_image_address=caretaker_upload(caretaker_image)
    db_animal = Animal(
        tag_id=tag_id,
        gender=gender,
        age=age,
        fitness=fitness,
        vaccination=vaccination,
        sterilisation=sterilisation,
        animal_type=animal_type,
        caretaker=caretaker,
        contact=contact,
        caretaker_whatsapp=whatsapp,
        caretaker_add=address,
        caretaker_social=social,
        caretaker_occ=occupation,
        caretaker_image=caretaker_image_address,
        photos=file_url  # Store uploaded file URL

    )
    db.add(db_animal)
    db.commit()
    #db.refresh(db_animal)
    return {"message": "Animal entry created successfully", "animal_id": db_animal.tag_id}

# Route to get all animal entries
@router.get("/animals/", response_model=List[dict])
def get_all_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    return [{"tag_id": animal.tag_id, "animal_type": animal.animal_type,"Caretaker": animal.caretaker,"contact":animal.contact, "photos": animal.photos,"avaliable":animal.available} for animal in animals]

# Route to get a single animal entry by ID
@router.get("/animals/{tag_id}", response_model=dict)
def get_animal(tag_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"tag_id":animal.tag_id,
            "age":animal.age,
            "type":animal.animal_type,
            "gender":animal.gender,
            "fitness":animal.fitness,
            "sterilisation":animal.sterilisation,
            "vaccination":animal.vaccination,
            "caretaker":animal.caretaker,
            "contact":animal.contact,
            "photos":animal.photos,
            "avaliable":animal.available}

# Route to update an animal entry
@router.put("/animals/{tag_id}", response_model=dict)
def update_animal(tag_id: int, animal: AnimalUpdate, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found") 
    db_animal.available=animal.available
    db.commit()
    #db.refresh(db_animal)
    return {"message": "Animal entry updated successfully", "animal_id": db_animal.tag_id}

# Route to delete an animal entry
@router.delete("/animals/{tag_id}", response_model=dict)
def delete_animal(tag_id: int, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(db_animal)
    db.commit()
    return {"message": "Animal entry deleted successfully"}
