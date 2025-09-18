from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class PredictIn(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)

class PredictOut(BaseModel):
    id: int
    text: str
    label: str
    score: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

    