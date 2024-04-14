from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.src.middleware.config import *
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class CriminalDao(Base):
    __tablename__ = 'criminal'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Boolean)
    image=Column(String)
    description =Column(String)







