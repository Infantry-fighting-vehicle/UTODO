from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, Text, JSON
from sqlalchemy.dialects.mysql import INTEGER

from models.User import User
# from . import GroupTask
# from . import GroupMember

from models.Base import Base


# Base = declarative_base()
# metadata = Base.metadata

class Group(Base):
    __tablename__ = "groups_"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))

    members = relationship("GroupMember", cascade="all, delete-orphan")
    group_tasks = relationship("GroupTask", cascade="all, delete-orphan")

class GroupMember(Base):
    __tablename__ = "groupMembers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    group_id = Column(Integer, ForeignKey("groups_.id", ondelete='CASCADE'))