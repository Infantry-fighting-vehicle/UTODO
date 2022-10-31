from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, text, JSON, Text
from sqlalchemy.dialects.mysql import INTEGER

from models.Group import Group
from models.User import User

Base = declarative_base()
metadata = Base.metadata

class GroupTask(Base):
    __tablename__ = "groupTasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    group_id =  Column(Integer, ForeignKey(Group.id))

class UserTask(Base):
    __tablename__ = "userTasks"

    id = Column(Integer, primary_key=True)
    status = Column(String(255))
    user_id = Column(Integer, ForeignKey(User.id))
    groupTask_id = Column(Integer, ForeignKey(Group.id))