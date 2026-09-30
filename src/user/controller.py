from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, status, Request, Depends
from pwdlib import PasswordHash
from src.utils.settings import settings
from src.utils.db import get_db
import jwt
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()
EXP_TIME = 30


def get_password_hash(password):
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):

    is_user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    is_user = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "registration done for": new_user.name
    }


# login flow
def login_user(body: LoginSchema, db: Session):

    user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found"
        )

    if not password_hash.verify(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password"
        )

    exp_time = datetime.now() + timedelta(minutes=EXP_TIME)

    token = jwt.encode({
        "_id": user.id,
        "exp": exp_time
    }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "token": token
    }


# token headers mai send hote hai
def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not Authorized to access this resource!"
            )
        token = token.split(" ")[-1]
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = data.get("_id")
        exp_time = data.get("exp")
        current_time = datetime.now().timestamp()
        if current_time > exp_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="EXPIRED token"
            )
        user = db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to access this resource!"
            )
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to access this resource!"
        )