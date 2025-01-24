from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Caretaker(Base):
    __tablename__ = 'caretaker'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    contact = Column(String)
    caretaker_whatsapp=Column(String)
    caretaker_add = Column(String)
    caretaker_social=Column(String)
    caretaker_occ=Column(String)
    caretaker_username=Column(String,unique=True)
    caretaker_pass=Column(String)
    status=Column(String, default='Offline')
    caretaker_image=Column(String)
    caretaker_signeture=Column(String)
    no_animals=Column(Integer,default=0)
    approved=Column(Enum('Pending', 'Approved','BlackListed', name='status_enum'),default="Pending")
    auth_token=Column(String,nullable=True)
class Animal(Base):
    __tablename__ = 'animals'
    id=Column(Integer,primary_key=True,autoincrement=True)
    caretaker_id=Column(Integer,ForeignKey('caretaker.id'))
    caretaker=relationship("Caretaker")
    tag_id=Column(String,unique=True)
    gender=Column(String,default="Not sure")
    age=Column(Integer)
    fitness=Column(String)
    vaccination=Column(Boolean)
    sterilisation=Column(Boolean)
    animal_type = Column(String)
    photos = Column(String)
    avaliable = Column(Boolean, default=True)

class Lead(Base):
    __tablename__='leads'
    id=Column(Integer,primary_key=True,autoincrement=True)
    tag_id=Column(String,ForeignKey('animals.tag_id'))
    animal = relationship("Animal")
    adopter_name = Column(String(225))
    contact=Column(String)
    whatsapp = Column(String)
    Email = Column(String)
    homeType = Column(String)
    Address = Column(String)
    Address_permanent=Column(String)
    occupation = Column(String(225))
    social=Column(String)
    adopter_image=Column(String)
    adopter_doc_front=Column(String)
    adopter_doc_back=Column(String)
    incamp=Column(String)
    status = Column(Enum('Pending', 'Approved', 'Denied','Cancled', name='status_enum'), default='Pending')
    remarks=Column(String)

class Application(Base):
    __tablename__='applications'
    id = Column(Integer, primary_key=True)
    tag_id=Column(Integer, ForeignKey('animals.id'))
    application_id=Column(Integer,ForeignKey('leads.id'))
    application=relationship("Lead")
    councler_name=Column(String)
    plans=Column(String)
    pets=Column(String)
    alone=Column(String)
    temp_caretaker=Column(String)
    caretaker_signeture=Column(String,nullable=True)
    adoptor_signeture=Column(String,nullable=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    role = Column(String(225))  # Can be 'Admin' or 'Team'
    password = Column(String(225))
    auth_token=Column(String,nullable=True)
    status = Column(String, default='Offline')