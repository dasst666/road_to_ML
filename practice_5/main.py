from contextlib import asynccontextmanager
import logging
import threading
from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from ml.model import get_pipeline, predict_label_score
from db.database import get_db
from models.predict import Predict
from schemas.predict import PredictIn, PredictOut
from prometheus_client import Counter, generate_latest
from starlette.responses import Response, PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator

logger = logging.getLogger("uvicorn.error")
REQUEST_COUNT = Counter("request_count", "Total number of requests")

def _warmup_job():
    try:
        logger.info("🔄 Warmup start...")
        get_pipeline()
        logger.info("✅ Warmup done")
    except Exception:
        logger.exception("Warmup failed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=_warmup_job, daemon=True).start()
    yield

app = FastAPI(title="Minimal Predict", lifespan=lifespan)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.inc()
    return response

@app.get("/ping")
def ping():
    return PlainTextResponse("pong")

@app.post("/predict", response_model=PredictOut, status_code=201)
def predict(payload: PredictIn, db: Session = Depends(get_db)):
    label, score = predict_label_score(payload.text)

    row = Predict(text=payload.text, label=label, score=score)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@app.get("/predict", response_model=List[PredictOut])
def get_predicts(db: Session = Depends(get_db)):
    predicts = db.query(Predict).all()
    return predicts

@app.get("/health")
def health():
    return {"status": "ok"}