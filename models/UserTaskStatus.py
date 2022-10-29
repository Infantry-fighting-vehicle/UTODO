from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP, text, JSON
from sqlalchemy.dialects.mysql import INTEGER
from models import Task, User

Base = declarative_base()
metadata = Base.metadata

class UserTaskStatus(Base):
    __tablename__ = "user-task-status"

    id = Column(Integer, primary_key=True)
    task = Column(Integer, ForeignKey(Task.id), primary_key=True)
    user = Column(Integer, ForeignKey(User.id), primary_key=True)
    status = Column(String(64))