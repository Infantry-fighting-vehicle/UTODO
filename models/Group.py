from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, Text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from models import User

Base = declarative_base()
metadata = Base.metadata

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    name = Column(String(255))
    owner_id = Column(Integer, ForeignKey(User.id), primary_key=True)