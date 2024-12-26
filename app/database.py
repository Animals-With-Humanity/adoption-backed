from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL should be changed to your database URL.
# Example for SQLite:
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://neondb_owner:xR7HX1DhlzvF@ep-wandering-scene-a7j5x3ak-pooler.ap-southeast-2.aws.neon.tech/neondb"
## Switch to deployment db 
#"postgresql://neondb_owner:W3FMILeyHkP0@ep-long-union-a5mh444q-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
Base: DeclarativeMeta = declarative_base()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
