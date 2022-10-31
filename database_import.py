from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

connection_string = 'mysql://root:000000@127.0.0.1:3306/utodolist'

engine = create_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

a = models.User(name="Stepan", surname="vald", email="text@example.com", password="superstrong")

print(a)
session.add(a)
session.commit()

# for class_instance in session.query(models.User).all():
#     print(vars(class_instance))
