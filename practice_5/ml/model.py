from functools import lru_cache
import os
from transformers import pipeline

DEFAULT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

@lru_cache(maxsize=1)
def get_pipeline():
    model_name = os.getenv("SENTIMENT_MODEL", DEFAULT_MODEL)
    # CPU по умолчанию (ничего дополнительно указывать не надо)
    return pipeline("sentiment-analysis", model=model_name)

def predict_label_score(text: str) -> tuple[str, float]:
    nlp = get_pipeline()
    out = nlp(text)[0]  # {'label': 'POSITIVE', 'score': 0.998...}
    return out["label"], float(out["score"])