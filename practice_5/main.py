from contextlib import asynccontextmanager
import logging
import threading
import time
from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session
from ml.model import get_pipeline, predict_label_score
from db.database import get_db
from models.predict import Predict
from schemas.predict import PredictIn, PredictOut


app = FastAPI(title="Minimal Predict")


logger = logging.getLogger("uvicorn.error")

def _warmup_job():
    try:
        logger.info("🔄 Warmup start...")
        get_pipeline()
        logger.info("✅ Warmup done")
    except Exception:
        logger.exception("Warmup failed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # запускаем прогрев в отдельном потоке и сразу отдаём управление
    threading.Thread(target=_warmup_job, daemon=True).start()
    yield  # приложение уже принимает запросы
    # (ничего на shutdown не делаем)

app = FastAPI(title="Minimal Predict", lifespan=lifespan)

@app.post("/predict", response_model=PredictOut, status_code=201)
def predict(payload: PredictIn, db: Session = Depends(get_db)):
    label, score = predict_label_score(payload.text)

    row = Predict(text=payload.text, label=label, score=score)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@app.get("/health")
def health():
    return {"status": "ok"}