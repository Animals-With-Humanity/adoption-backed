from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Animal(Base):
    __tablename__ = 'animals'
    #id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, primary_key=True,unique=True, index=True)
    gender=Column(String,default="Not sure")
    age=Column(Integer)
    fitness=Column(String)
    vaccination=Column(Boolean)
    sterilisation=Column(Boolean)
    animal_type = Column(String)
    caretaker = Column(String,nullable=False)
    contact = Column(String)
    caretaker_whatsapp=Column(String)
    caretaker_add = Column(String)
    caretaker_social=Column(String) 
    caretaker_occ=Column(String)
    caretaker_image=Column(String)
    photos = Column(String)
    available = Column(Boolean, default=True)

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('animals.tag_id'))
    animal = relationship("Animal")
    adopter_name = Column(String(225))
    contact=Column(String)
    whatsapp = Column(String)
    Email = Column(String)
    homeType = Column(String)
    Address = Column(String)
    occupation = Column(String(225))
    social=Column(String)
    adopter_image=Column(String)
    adopter_doc=Column(String)
    incamp=Column(String)
    status = Column(Enum('Pending', 'Approved', 'Denied', name='status_enum'), default='Pending')

class GenralInfo(Base):
    __tablename__ ="genralinfo"
    track_id = Column(Integer, primary_key=True)
    tag_id=Column(Integer, ForeignKey('animals.tag_id'))
    application_id=Column(Integer,ForeignKey('applications.id'))
    application=relationship("Application")
    councler_name=Column(String)
    plans=Column(String)
    pets=Column(String)
    alone=Column(String)
    temp_caretaker=Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    role = Column(String(225))  # Can be 'Admin' or 'Team'
    password = Column(String(225))
    status = Column(String, default='Offline')
