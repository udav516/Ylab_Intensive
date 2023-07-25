from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://postgres:EY8oqoMW_B@localhost:5432/postgres')
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    session = Session()
    Base.metadata.create_all(engine)
    try:
        yield session
    finally:
        session.close()
