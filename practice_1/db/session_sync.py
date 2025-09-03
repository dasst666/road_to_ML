from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from practice_1.config import settings

engine = create_engine(
    settings.DATABASE_URL_SYNC,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)