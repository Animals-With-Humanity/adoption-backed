from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Animal(Base):
    __tablename__ = 'animals'
    #id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, primary_key=True,unique=True, index=True)
    animal_type = Column(String(225))
    caretaker = Column(String,nullable=False)
    contact = Column(String)
    photos = Column(String(225))
    available = Column(Boolean, default=True)

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('animals.tag_id'))
    animal = relationship("Animal")
    adopter_name = Column(String(225))
    contact=Column(String)
    whatsapp = Column(String)
    Address = Column(String)
    occupation = Column(String(225))
    pets = Column(Boolean,default=False)
    homeType = Column(String)
    status = Column(Enum('Pending', 'Approved', 'Denied', name='status_enum'), default='Pending')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))
    role = Column(String(225))  # Can be 'Admin' or 'Team'
    password=Column(String(225))
    status=Column(Enum('Online', 'Offline', name='status_enum'), default='Offline')

