from pydantic import BaseModel, Field, field_validator

MAX_TEXT_LEN = 5000
FORBIDDEN_CHARS = set("\0")

class TextIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_LEN)

    @field_validator("text")
    def strip_and_check(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Текст пустой после trip()")
        if any(ch in FORBIDDEN_CHARS for ch in v):
            raise ValueError("Недопустимые символы во входном тексте")
        return v