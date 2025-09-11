from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

data = {
    1: {"name": "to do homework"},
}

@router.get("/")
def show_task():
    return data

@router.get("/{task_id}")
def show_task(task_id: int):
    return data.get(task_id)