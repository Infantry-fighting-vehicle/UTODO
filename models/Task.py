from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, text, JSON, Text
from sqlalchemy.dialects.mysql import INTEGER

from models.Group import Group
from models.User import User
# from models.Task import UserTask

from models.Base import Base


# Base = declarative_base()
# metadata = Base.metadata

class GroupTask(Base):
    __tablename__ = "groupTasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    group_id =  Column(Integer, ForeignKey("groups_.id", ondelete='CASCADE'))

    user_tasks = relationship("UserTask", cascade="all, delete-orphan")

class UserTask(Base):
    __tablename__ = "userTasks"

    id = Column(Integer, primary_key=True)
    status = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    groupTask_id = Column(Integer, ForeignKey("groupTasks.id", ondelete='CASCADE'))

