from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))