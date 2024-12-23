from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import base

DATABASE_URL = "sqlite:///lenClients.db"

engine = create_engine(DATABASE_URL)
base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
