import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_session
from models.tasks import Task
from database.cache import build_cache_key, get_redis, ttl_with_jitter
from schemas.tasks import TaskCreate, TaskPublic, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# @router.get("/", response_model=List[TaskPublic])
# async def show_task(session: AsyncSession =  Depends(get_session)):
#     result = await session.execute(select(Task))
#     tasks = result.scalars().all()
#     return tasks

@router.get("/", response_model=List[TaskPublic])
async def show_task(response: Response, session: AsyncSession = Depends(get_session)):
    r = await get_redis()
    key = build_cache_key("tasks")  # или "tasks:all"

    # 1) пробуем из кеша
    cached = await r.get(key)
    if cached:
        response.headers["X-Cache"] = "HIT"
        return [TaskPublic.model_validate(obj) for obj in json.loads(cached)]

    # 2) БД
    result = await session.execute(select(Task))
    tasks = result.scalars().all()

    # 3) в Redis кладём JSON-совместимые dict’ы
    payload = [TaskPublic.model_validate(t).model_dump(mode="json") for t in tasks]
    await r.set(key, json.dumps(payload), ex=ttl_with_jitter())

    # можно вернуть payload (FastAPI сам приведёт под response_model)
    return payload

@router.get("/{task_id}", response_model=TaskPublic)
async def show_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Такой записи нету")
    return task

@router.post("/", response_model=TaskPublic, status_code=201)
async def create_task(payload: TaskCreate, session: AsyncSession = Depends(get_session)):
    task = Task(**payload.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    r = await get_redis() #redis
    await r.delete(build_cache_key("tasks")) #redis
    return task

@router.patch("/{task_id}", response_model=TaskPublic)
async def update_task(task_id: int, payload: TaskUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Такой записи не существует")
    
    data = payload.model_dump(exclude_unset=True, exclude={"id"})

    for k,v in data.items():
        setattr(task, k, v)
    
    await session.commit()
    await session.refresh(task)
    return task
