from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()
load_dotenv(override=False)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    PG_USER = os.getenv("POSTGRES_USER", "postgres")
    PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
    PG_HOST = os.getenv("DB_HOST", "db")      
    PG_PORT = os.getenv("DB_PORT", "5432")
    PG_DB = os.getenv("POSTGRES_DB", "predict_db")
    DATABASE_URL = f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()