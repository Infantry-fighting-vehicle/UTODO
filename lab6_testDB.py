from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import get_session
import models

session = get_session()

a = models.User(name="Stepan", surname="vald", email="text@example.com", password="superstrong")

print(a)
session.add(a)
session.commit()

for class_instance in session.query(models.User).all():
    print(vars(class_instance))
