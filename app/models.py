from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Animal(Base):
    __tablename__ = 'animals'
    #id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, primary_key=True,unique=True, index=True)
    animal_type = Column(String)
    photos = Column(String)
    available = Column(Boolean, default=True)

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True)
    adopter_name = Column(String)
    occupation = Column(String)
    tag_id = Column(Integer, ForeignKey('animals.tag_id'))
    status = Column(Enum('Pending', 'Approved', 'Denied', name='status_enum'), default='Pending')
    animal = relationship("Animal")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)  # Can be 'Admin' or 'Team'
    password=Column(String)
    status=Column(Enum('Online', 'Offline', name='status_enum'), default='Offline')

