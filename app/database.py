from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Load DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create DB engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models to inherit
Base = declarative_base()

# Dependency to get DB session (for routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
