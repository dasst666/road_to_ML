from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_session
from models.tasks import Task
from schemas.tasks import TaskCreate, TaskPublic, TaskPublicNoID, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])

# как лист
data = [
    {"id": 1, "title": "work", "content": "to do homework"},
    {"id": 2, "title": "study", "content": "to do homework"},
    {"id": 3, "title": "life", "content": "to do homework"},
]

# как словарь
data_dict = {
    1: {"title": "work", "content": "to do homework"},
    2: {"title": "study", "content": "to do homework"},
    3: {"title": "life", "content": "to do homework"},
}

@router.get("/", response_model=dict[int, TaskPublicNoID])
def show_task():
    return data_dict

# @router.get("/", response_model=list[TaskPublic])
# def show_task():
#     return data

@router.get("/{task_id}", response_model=TaskPublicNoID)
def show_task(task_id: int):
    return data_dict.get(task_id)

@router.post("/", response_model=TaskPublic, status_code=201)
async def create_task(payload: TaskCreate, session: AsyncSession = Depends(get_session)):
    task = Task(title=payload.title, content = payload.content)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskPublicNoID)
def update_task(task_id: int, payload: TaskUpdate):
    task_dict = payload.model_dump()
    if task_dict.id != task_id:
        raise HTTPException(status_code=400, detail="ID не совпадают")
    if task_dict.id not in  data_dict:
        raise HTTPException(status_code=404, detail="Такой записи не существует")
    data_dict[payload.id] = task_dict