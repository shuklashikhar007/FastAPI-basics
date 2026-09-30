# yaha par database connections ko configure karege ham 
from sqlalchemy import create_engine
from src.utils.settings import settings
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()

engine = create_engine(url = settings.DB_CONNECTION)

LocalSession = sessionmaker(bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
