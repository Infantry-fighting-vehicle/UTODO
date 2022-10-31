from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, Text, JSON
from sqlalchemy.dialects.mysql import INTEGER

from models.User import User

Base = declarative_base()
metadata = Base.metadata

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey(User.id))

class GroupMember(Base):
    __tablename__ = "groupMembers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.id), primary_key=True)