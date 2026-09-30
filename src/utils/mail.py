from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email : List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "l1M8T@example.com",
    MAIL_PASSWORD = "password",
    MAIL_FROM = "l1M8T@example.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False
)