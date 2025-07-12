from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

#engine = create_engine(
#    "sqlite:///./test.db",
#    connect_args={"check_same_thread": False}
#)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
