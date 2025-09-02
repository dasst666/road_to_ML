from typing import Annotated, Union
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

from enum import Enum

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Dastan"}

# Try to write Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep lerning FTW!"}
    elif model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# Write query params

@app.get("/items/{item_id}")
async def get_items(item_id: int, needed: str, not_needed: str | None = None, is_enable: bool = True, stery: str | None = None):
    if not_needed:
        return {"item_id": item_id, "needed": needed, "not_needed": not_needed, "enable_status": is_enable, "just": stery}
    return {"item_id": item_id, "needed": needed, "enable_status": is_enable, "just": stery}


class Item(BaseModel):
    name: str
    quantity: int
    price: float # bigger than 0 at least
    description: Union[str, None] = None
    is_active: bool = False

@app.post("/items/{user_id}")
async def create_items(user_id: int, item: Item):
    item_dict = item.model_dump()
    if item.quantity > 0:
        all_price = item.quantity * item.price
        item_dict.update({"all_items_price": all_price})
    return item_dict

# Mini crud
data = {
    1: {"name": "Alice", "age": 25},
    2: {"name": "Bob", "age": 30},
    3: {"name": "Charlie", "age": 22},
}

class User(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=2, max_length=50)] 
    age: Annotated[int, Field(ge=1, le=150)]

@app.get("/users/", response_model=User)
async def get_all_users():
    return data

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    # if user_id in data:
    #     return data[user_id]
    return data.get(user_id)
    
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in data:
        raise HTTPException(status_code=400, detail="User already exists")
    data[user.id] = {"name": user.name, "age": user.age}
    return data[user.id]

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User id in path and body must be same")
    if user.id not in data:
        raise HTTPException(status_code=404, detail="User not found")
    data[user_id] = {"name": user.name, "age": user.age}
    return data[user_id]

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    if user_id in data:
        deleted = data.pop(user_id)
        return deleted
    raise HTTPException(status_code=404, detail="User not found")
    