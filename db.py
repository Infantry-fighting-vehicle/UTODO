from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# session = 'temp_init_holder'


def session_init():
    # connection_string = 'mysql://root:000000@127.0.0.1:3306/utodolist'
    connection_string = 'mysql://startup:hû$§Ó]Çýf¬Y3~XÓ¡:/["pÖ9Ý<@127.0.0.1:3307/utodolist'
    engine = create_engine(connection_string, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

session = session_init()

def get_session():
    session.flush()
    return session