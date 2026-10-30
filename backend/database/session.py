from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.core.config import settings


# Check whether the database URL exists
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured")


# Create the database engine
engine = create_engine(settings.DATABASE_URL)


# Create a database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for database models
Base = declarative_base()


# Database dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()