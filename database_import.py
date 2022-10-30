from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

connection_string = 'mysql://startup:pass@127.0.0.1/utodolist'

engine = create_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

a = User(name="Stepan", surname="vald", email="text@example.com", password="superstrong")

print(a)
session.add(a)
session.commit()

for class_instance in session.query(User).all():
    print(vars(class_instance))
