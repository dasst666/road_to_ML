from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def on_startup():
    from database.db import init_models
    await init_models()

app.include_router(users.router)
app.include_router(tasks.router)
