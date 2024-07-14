from sqlalchemy import Column, Integer, String, Boolean, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean)

class Cards(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    balance = Column(String)

class Fees(Base):
    __tablename__ = 'fees'
    id = Column(Integer, primary_key=True)
    fee = Column(Double)