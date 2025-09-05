from celery_app import celery_app
import time

@celery_app.task
def hello(name: str) -> str:
    # Симулируем долгую работу
    time.sleep(2)
    return f"Hello, {name}!"