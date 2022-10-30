from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, text, JSON, Text
from sqlalchemy.dialects.mysql import INTEGER
from models.Group import Group

Base = declarative_base()
metadata = Base.metadata

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    group =  Column(Integer, ForeignKey(Group.id), primary_key=True)
    name = Column(String(255))
    description = Column(Text)