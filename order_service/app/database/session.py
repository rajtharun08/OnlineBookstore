import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    retries = 5
    while retries > 0:
        try:
            # This is what creates your tables in Postgres
            Base.metadata.create_all(bind=engine) 
            print("Tables created successfully!")
            break
        except OperationalError:
            print("Database not ready, retrying in 2 seconds...")
            retries -= 1
            time.sleep(2)
    if retries == 0:
        print("Could not connect to the database. Exiting.")