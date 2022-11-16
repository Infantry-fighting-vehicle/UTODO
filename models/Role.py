from sqlalchemy import Column, ForeignKey, String, Integer
from models.Base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    value = Column(String(100))