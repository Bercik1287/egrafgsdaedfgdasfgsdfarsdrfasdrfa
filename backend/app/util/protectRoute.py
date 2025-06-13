from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.userService import UserService
from app.core.database import get_db
from app.db.schema.user import UserOutput
from decouple import config

AUTH_PREFIX = config("AUTH_PREFIX")

def get_current_user(
        session: Session = Depends(get_db), 
        authorisation: Annotated[Union[str, None], Header()] = None
) -> UserOutput:
    auth_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )

    if not authorisation:
        raise auth_exception
    
    if not authorisation.startswith(AUTH_PREFIX):
        raise auth_exception
    
    payload = AuthHandler.decde_jwt(token=authorisation[len(AUTH_PREFIX):])

    if payload and payload["user_id"]:
        try:
            user = UserService(session=session).get_user_by_id(payload["user_id"])
            return UserOutput(
                id= user.id,
                username= user.username,
                email= user.email
            )
        except Exception as error:
            raise error
    
    raise auth_exception