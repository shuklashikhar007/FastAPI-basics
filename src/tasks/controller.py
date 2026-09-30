from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session 
from src.tasks.models import TaskModel
from src.user.models import UserModel
from fastapi import HTTPException
from src.utils.helpers import is_authenticated
def create_task(body:TaskSchema, db: Session, user:UserModel):
 data = body.model_dump() # data will be converted to a python dict
 new_task = TaskModel(title = data["title"], 
                      description = data["description"], 
                      is_completed = data["is_completed"]
                      , user_id = user.id)
 db.add(new_task)
 db.commit()
 db.refresh(new_task)
 return{
    "status":"task created successfully",
      "task": new_task
    }

def get_tasks(db:Session,user:UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all() # jo user logged in hai usi ke tasks show karo 
    return {
       "sare ke sare tasks" : tasks
    }

def get_one_task(task_id:int,db:Session):
   one_task = db.query(TaskModel).get(task_id)
   if not one_task:
      raise HTTPException(status_code = 404, detail = "task not found")
   return {
      "status" : "task found successfully",
      "task" : one_task
   }

def delete_task(task_id:int,db:Session):
   one_task = db.query(TaskModel).get(task_id)
   if not one_task:
      raise HTTPException(status_code = 404, detail = "task not found")
   db.delete(one_task)
   db.commit()
   return {
      "status" : "task deleted successfully"
   }

def update_task(task_id:int,body:TaskSchema,db:Session):
   one_task = db.query(TaskModel).get(task_id)
   if not one_task:
      raise HTTPException(status_code = 404, detail = "task not found")
   data = body.model_dump() # convert the incoming data to a python dict
   one_task.title = data["title"]
   one_task.description = data["description"]
   one_task.is_completed = data["is_completed"]
   db.commit() # to save the changes
   return {
      "status" : "task updated successfully",
      "task" : one_task
   }