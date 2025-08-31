from fastapi import FastAPI

from enum import Enum

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Dastan"}

@app.get("/users/{user_id}")
async def get_user(user_id: int, is_active: bool = True):
    return {"user_id": user_id, "active_status": is_active}

# Try to write Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep lerning FTW!"}
    elif model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
