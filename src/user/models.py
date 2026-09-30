# sari data validation files yaha par store hogi 
from sqlalchemy import Column, Integer , String , Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    hash_password = Column(String, nullable=False)
    email = Column(String)