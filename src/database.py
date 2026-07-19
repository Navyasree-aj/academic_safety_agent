# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

# Adjust the connection URL to use our modern psycopg driver
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Build connection engine with stability ping configurations
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Generate a transaction session generator factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class mapping our Python classes directly to database rows
Base = declarative_base()

def get_db():
    """Context utility to provide isolated database transaction scopes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Instructs SQLAlchemy to scan metadata models and physically 
    generate any missing tables (like syllabus_log) inside PostgreSQL.
    """
    # Inline imports ensure that SQLAlchemy registers your models onto Base before table creation
    from src.models import Student, AcademicMetric, SyllabusLog
    
    print("⏳ Syncing database metadata schemas with PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables successfully synchronized!")