import logging
import time
from fastapi import FastAPI, Request

from ml.model import predict_label_score
from schemas.predict import PredictIn, PredictOut


app = FastAPI(title="Minimal Predict")


logger = logging.getLogger("uvicorn.error")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    logger.info("➡️ START %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        return response
    finally:
        dur_ms = (time.time() - start) * 1000
        # response может быть не определён если исключение выше — поэтому в finally пишем осторожно
        status = getattr(locals().get("response", None), "status_code", "-")
        logger.info("✅ END   %s %s -> %s (%.1f ms)", request.method, request.url.path, status, dur_ms)

@app.on_event("startup")
def warmup():
    from ml.model import get_pipeline
    """Прогреваем пайплайн, но не валим приложение при ошибке."""
    try:
        _ = get_pipeline()  # инициализация модели/токенайзера
        logger.info("🧊 Warmed up sentiment pipeline")
    except Exception:
        logger.exception("Warmup failed — продолжим без прогрева")

@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    label, score = predict_label_score(payload.text)
    return PredictOut(label=label, score=score)