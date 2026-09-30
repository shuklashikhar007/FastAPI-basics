from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db 
from src.utils.helpers import is_authenticated
from src.user.models import UserModel
# complete CRUD operations
task_routes = APIRouter(prefix="/tasks") # prefix of sare task related routes jo banaye jayege iske agge
# post endpoint
@task_routes.post("/create", status_code = status.HTTP_201_CREATED)
# first part is validation schema second part is 
# dependency injection part 
def create_task(body:TaskSchema, db = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.create_task(body,db,user)
# get end-point
# is_authenticated function will be put as a dependency injection 
# sare ke sare function mai idhar 
@task_routes.get("/all_tasks", status_code = status.HTTP_200_OK)
def get_all_tasks(db = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db,user)
@task_routes.get("/task/{task_id}", status_code = status.HTTP_200_OK)
def get_one_task(task_id:int,db = Depends(get_db)):
    return controller.get_one_task(task_id,db)
@task_routes.put("/update/{task_id}",status_code = status.HTTP_201_CREATED)
def update_task(task_id:int,body:TaskSchema,db = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.update_task(task_id,body,db)
@task_routes.delete("/delete/{task_id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.delete_task(task_id,db)