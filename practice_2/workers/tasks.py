# workers/tasks.py
import re
from datetime import datetime
from celery import states
from workers.celery_app import celery_app
from db.database import SessionLocal
from sqlalchemy import select
from schemas.task_parse_text import TaskResult 
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="workers.tasks.hello")
def hello(name: str) -> str:
    import time
    time.sleep(2)
    return f"Hello, {name}!"

@celery_app.task(bind=True, name="workers.tasks.parse_text", autoretry_for=(), retry_kwargs={"max_retries": 0})
def parse_text(self, text: str):
    task_id = self.request.id

    # старт задачи → обновим запись, если она есть
    with SessionLocal() as session:
        row = session.execute(
            select(TaskResult).where(TaskResult.task_id == task_id)
        ).scalar_one_or_none()
        if row:
            row.status = states.STARTED
            session.add(row)
            session.commit()

    try:
        cleaned_text = re.sub(r"[!,.?@+\-/><%:;]", "", text.lower())
        words = cleaned_text.split()
        words_counter = len(words)
        unique_words_counter = len(set(words))
        symbols_counter = len(re.findall(r"[!,.?@+\-/><%:;]", text))
        longest_word = max(words, key=len) if words else ""

        result = {
            "words count": words_counter,
            "longest word": longest_word,
            "unique words count": unique_words_counter,
            "symbols count": symbols_counter,
        }

        logger.info(
            "Parsed text: words=%s unique=%s symbols=%s longest=%s",
            words_counter, unique_words_counter, symbols_counter, longest_word
        )

        # финиш задачи → сохраняем результат
        with SessionLocal() as session:
            row = session.execute(
                select(TaskResult).where(TaskResult.task_id == task_id)
            ).scalar_one_or_none()
            if row:
                row.status = states.SUCCESS
                row.result = result
                row.finished_at = datetime.utcnow()
                session.add(row)
                session.commit()

        return result

    except Exception as e:
        # ошибка → зафиксируем её
        with SessionLocal() as session:
            row = session.execute(
                select(TaskResult).where(TaskResult.task_id == task_id)
            ).scalar_one_or_none()
            if row:
                row.status = states.FAILURE
                row.error = str(e)
                row.finished_at = datetime.utcnow()
                session.add(row)
                session.commit()
        raise