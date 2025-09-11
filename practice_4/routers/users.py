from fastapi import APIRouter, HTTPException
from schemas.users import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

data = {
    1: {"name": "Cristiano Ronaldo", "age": 40, "password": 123456789},
    2: {"name": "Lionel Messi", "age": 40, "password": 123456789}
}

@router.get("/", response_model=UserPublic)
def show_users():
    return data

@router.get("/{user_id}", response_model=UserPublic)
def show_user(user_id: int):
    return data.get(user_id)

@router.post("/", response_model=UserPublic)
def create_user(payload: UserCreate):
    user_dict = payload.model_dump()
    if payload.id in data:
        raise HTTPException(status_code=404, detail="Пользователь уже существует")
    data[payload.id] = user_dict
    return data[payload.id]

@router.put("/{user_id}", response_model=UserPublic)
def update_user(payload: UserUpdate, user_id: int):
    user_dict = payload.model_dump()
    if payload.id != user_id:
        raise HTTPException(status_code=400, detail="ID не совпадают")
    if payload.id not in data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    data[payload.id] = user_dict
    return data[payload.id]

@router.delete("/{user_id}", response_model=UserPublic)
def delete_user(user_id: int):
    if user_id in data:
        deleted = data.pop(user_id)
        return deleted
    raise HTTPException(status_code=404, detail="Пользователь не найден")