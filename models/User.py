from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER

# from models.Group import Group, GroupMember
# from models.Task import UserTask

from models.Base import Base


# Base = declarative_base()
# metadata = Base.metadata

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    memberships = relationship("GroupMember", cascade="all, delete-orphan")
    groups = relationship("Group", cascade="all, delete-orphan")
    user_tasks = relationship("UserTask", cascade="all, delete-orphan")
    