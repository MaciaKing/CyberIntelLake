from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.file_progress import Base
import os

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
               f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create table on db
Base.metadata.create_all(bind=engine)
