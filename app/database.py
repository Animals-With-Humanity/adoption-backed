from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL should be changed to your database URL.
# Example for SQLite:
SQLALCHEMY_DATABASE_URL =  "sqlite:///./app.db"
#"mysql+pymysql://sql12744654:aWGnxPRe1l@sql12.freesqldatabase.com:3306/sql12744654"
# Example for PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

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
