import datetime
from sqlalchemy import select
from db.database import SessionLocal
from schemas.task_parse_text import TaskResult
from .celery_app import celery_app
import time
import re
from celery import states

import logging

logger = logging.getLogger(__name__)

@celery_app.task
def hello(name: str) -> str:
    # Симулируем долгую работу
    time.sleep(2)
    return f"Hello, {name}!"

@celery_app.task(name="workers.tasks.parse_text")
def parse_text(self, text: str): 
    session = SessionLocal()

    try:
        row = session.execute(
            select(TaskResult).where(TaskResult.task_id == self.request.id)
        )
        if row:
            row.status = states.STARTED
            session.add(row)
            session.commit
    finally:
        session.close()
    
    try:
        cleaned_text = re.sub(r"[!,.?@+\-/><%:;]", "", text.lower())
        words = cleaned_text.split()
        
        words_counter = len(words)
        unique_words_counter = len(set(words))
        symbols_counter = len(re.findall(r"[!,.?@+\-/><%:;]", text))
        longest_word = max(words, key=len) if words else ""

        logger.info(f"Parsed text: {words_counter} words")
        logger.info(f"Parsed text longest word: {longest_word}")
        logger.info(f"Parsed text: {unique_words_counter} unique words")
        logger.info(f"Parsed text: {symbols_counter} symbols")

        result = {
                "words count": words_counter, 
                "longest word": longest_word, 
                "unique words count": unique_words_counter, 
                "symbols count": symbols_counter
                }

        session = SessionLocal()
        try:
            row = session.execute(
                select(TaskResult).where(TaskResult.task_id == self.request.id)
            ).scalar_one_or_none
            
            if row:
                row.status = states.SUCCESS
                row.result = result
                row.finished_at = datetime.utcnow()
                session.add(row)
                session.commit()
        finally: 
            session.close()
        
        return result
    except Exception as e:
        session = SessionLocal()
        try:
            row = session.execute(
                select(TaskResult).where(TaskResult.task_id == self.request.id)
            ).scalar_one_or_none()
            if row:
                row.status = states.FAILURE
                row.error = str(e)
                row.finished_at = datetime.utcnow()
                session.add(row)
                session.commit()
        finally:
            session.close()
        raise

