from fastapi import APIRouter, HTTPException

from schemas.tasks import TaskCreate, TaskPublic, TaskPublicNoID


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

@router.post("/", response_model=TaskPublic)
def create_task(payload: TaskCreate):
    task_dict = payload.model_dump()
    data_dict[payload.id] = task_dict
    return data_dict[payload.id]