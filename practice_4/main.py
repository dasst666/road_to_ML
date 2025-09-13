from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    from database.db import init_models
    await init_models()
    yield

app = FastAPI(lifespan=lifespan)
    

app.include_router(users.router)
app.include_router(tasks.router)
