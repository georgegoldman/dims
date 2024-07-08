import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Define the DATABASE_URL as a default argument
def SessionLocal(DATABASE_URL="sqlite:///./test.db"):
    database = Database(DATABASE_URL)
    metadata = MetaData()
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    class Idea(Base):
        __tablename__ = "ideas"

        id = Column(Integer, primary_key=True, index=True)
        description = Column(String, index=True)
        creator = Column(String, index=True)
        timestamp = Column(Integer)

    Base.metadata.create_all(bind=engine)

    return SessionLocal()