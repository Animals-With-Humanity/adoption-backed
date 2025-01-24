from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal,Caretaker
from pydantic import BaseModel
from typing import List
from utils import animal_upload
from datetime import datetime as dt

# Create the FastAPI router
router = APIRouter()

# Pydantic schema for updating the availability of an animal
class AnimalUpdate(BaseModel):
    age: int 
    fitness: str 
    vaccination: bool 
    sterilisation: bool
    avaliable:bool

# Route to create a new animal entry
@router.post("/animals/", response_model=dict)
def create_animal(
    id: int = Form(...),
    #tag_id: str = Form(...),
    gender: str = Form("Not sure"),
    age: int = Form(...),
    fitness: str = Form(...),
    vaccination: bool = Form(...),
    sterilisation: bool = Form(...),
    animal_type: str = Form(...),
    animal: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Upload the file and get the URL
    file_url =  animal_upload(animal)
    # Create a new animal entry
    db_caretaker=db.query(Caretaker).filter(Caretaker.id==id).first()
    animal_no=db_caretaker.no_animals
    tag_id=f'{dt.now().strftime("%Y.%m.%d")}.{id}.{animal_no+1}'
    db_animal = Animal(
        caretaker_id=id,
        tag_id=tag_id,
        gender=gender,
        age=age,
        fitness=fitness,
        vaccination=vaccination,
        sterilisation=sterilisation,
        animal_type=animal_type,
        photos=file_url,
    )
    db.add(db_animal)
    db_caretaker.no_animals=animal_no+1
    db.commit()
    db.refresh(db_animal)
    return {"message": "Animal entry created successfully", "id": tag_id}

# Route to get all animal entries
@router.get("/animals/", response_model=List[dict])
def get_all_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    approved_animals=[]
    for animal in animals:
        caretaker=db.query(Caretaker).filter(Caretaker.id==animal.caretaker_id).first()
        if caretaker.approved=="Approved":
            approved_animals.append(animal)
    return [
        {
            "id": animal.id,
            "caretaker_id": animal.caretaker_id,
            "tag_id": animal.tag_id,
            "animal_type": animal.animal_type,
            "gender": animal.gender,
            "age": animal.age,
            "fitness": animal.fitness,
            "vaccination": animal.vaccination,
            "sterilisation": animal.sterilisation,
            "photos": animal.photos,
            "avaliable": animal.avaliable,
        }
        for animal in approved_animals
    ]

# Route to get a single animal entry by ID
@router.get("/animals/{tag_id}", response_model=dict)
def get_animal(tag_id: str, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {
        "id": animal.id,
        "caretaker_id": animal.caretaker_id,
        "tag_id": animal.tag_id,
        "gender": animal.gender,
        "age": animal.age,
        "fitness": animal.fitness,
        "vaccination": animal.vaccination,
        "sterilisation": animal.sterilisation,
        "animal_type": animal.animal_type,
        "photos": animal.photos,
        "avaliable": animal.avaliable,
    }

# Route to update an animal entry
@router.put("/animals/{tag_id}", response_model=dict)
def update_animal(tag_id: str, animal_update: AnimalUpdate, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.tag_id == tag_id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db_animal.age=animal_update.age
    db_animal.fitness=animal_update.fitness 
    db_animal.vaccination=animal_update.vaccination
    db_animal.sterilisation=animal_update.sterilisation
    db_animal.avaliable=animal_update.avaliable
    db.commit()
    db.refresh(db_animal)
    return {"message": "Animal entry updated successfully", "animal_id": db_animal.id}

# Route to delete an animal entry
@router.delete("/animals/{id}", response_model=dict)
def delete_animal(id: int, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.id == id).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(db_animal)
    db.commit()
    return {"message": "Animal entry deleted successfully"}
