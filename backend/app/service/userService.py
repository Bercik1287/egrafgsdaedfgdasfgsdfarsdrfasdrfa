from app.db.repository.userRepo import AuthRepository
from app.db.schema.user import UserOutput, UserInCreate, UserInLogin, UserWithToken
from app.db.schema.autobus import AutobusInCreate, AutobusOutput,  BrygadaInCreate, BrygadaOutput, KierowcaInCreate, KierowcaOutput, LiniaInCreate, LiniaOutput, PrzystanekInCreate, PrzystanekOutput,TrasaInCreate, TrasaOutput, WariantInCreate, WariantOutput
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, session: Session):
        self.__authRepository__ = AuthRepository(session=session)
    
    def signup(self, user_details: UserInCreate) -> UserOutput:
        if self.__authRepository__.user_exist_by_username(username=user_details.username):
            raise HTTPException(status_code=400, detail="Please Login")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__authRepository__.create_user(user_data=user_details)
    
    def login(self, login_details: UserInLogin) -> UserWithToken:
        if not self.__authRepository__.user_exist_by_username(username=login_details.username):
            raise HTTPException(status_code=400, detail="Please Register")
        
        user = self.__authRepository__.get_user_by_username(username=login_details.username)
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request")
        raise HTTPException(status_code=400, detail="Please check your Credentials")
    
    def get_user_by_id(self, user_id: int):
        user = self.__authRepository__.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400, detail="User is not available")
    