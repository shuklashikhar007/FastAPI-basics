# command to start the server -> uvicorn main:app --reload
# SQLAlchemy -> ORM for PostgreSQL
# pydantic_settings -> library to import the env variables of the project 
from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes
from src.user.router import user_routes
Base.metadata.create_all(engine)
app = FastAPI(title ="FastAPI", version = "1.0.0")
app.include_router(task_routes)
app.include_router(user_routes)

