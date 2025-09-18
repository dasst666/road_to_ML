from datetime import datetime
from sqlalchemy import DateTime, Float, String, func
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Predict(Base):
    __tablename__ = "predicts"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
        )
