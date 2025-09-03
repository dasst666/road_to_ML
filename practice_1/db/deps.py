from collections.abc import Generator
from sqlalchemy.orm import Session
from practice_1.db.session_sync import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
        