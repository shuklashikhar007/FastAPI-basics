from fastapi import Request, HTTPException, status, Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
from src.utils.db import get_db
import jwt
from datetime import datetime, timedelta
# now this function will be used as a middleware to handle authenticated route everywhere
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