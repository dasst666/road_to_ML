from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_session
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskPublic, TaskPublicNoID, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskPublic])
async def show_task(session: AsyncSession =  Depends(get_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskPublicNoID)
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
