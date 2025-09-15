import os, json, hashlib, random
from typing import Any, Dict
from redis import asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "45"))

redis: aioredis.Redis | None = None

async def get_redis() -> aioredis.Redis:
    global redis
    if redis is None:
        redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis

def ttl_with_jitter(base: int | None = None) -> int:
    base = base or CACHE_TTL_SECONDS
    return base + random.randint(0, 10)

def build_cache_key(name: str, params: Dict[str, Any] | None = None) -> str:
    if not params:
        return f"{name}:all"
    payload = json.dumps(params, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return f"{name}:{h}"