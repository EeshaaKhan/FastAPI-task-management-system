from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

DATABASE_URL = settings.DATABASE_URL

# For SQLite, don't use StaticPool for normal file-based DB
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()  # commit after request ends
    except:
        db.rollback()
        raise
    finally:
        db.close()


def create_database() -> None:
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_database() -> None:
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)
