# routes hold karne wali file
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,LoginSchema
from src.user import controller
from src.utils import db
from src.utils.db import get_db
user_routes = APIRouter(prefix="/user")
@user_routes.post("/register",status_code = status.HTTP_201_CREATED)
def register(body:UserSchema,db = Depends(get_db)):
    return controller.register(body,db)
@user_routes.post("/login",status_code = status.HTTP_200_OK)
def login(body:LoginSchema,db = Depends(get_db)):
    return controller.login_user(body,db)
@user_routes.get("/is_auth")
def is_auth(request:Request, db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db) 
