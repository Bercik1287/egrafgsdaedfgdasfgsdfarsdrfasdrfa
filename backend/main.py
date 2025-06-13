from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput
from fastapi.middleware.cors import CORSMiddleware
from app.routers.autobusy import router
from app.routers.pdf_generator import router as pdf_router

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Created")
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["autentykacja"], prefix="/auth")

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return{"status": "Running..."}

@app.get("/protected")
def read_protected(user: UserOutput = Depends(get_current_user)):
    return{"status": "Running..."}

app.include_router(router)
app.include_router(pdf_router)

@app.get("/")
def root():
    return {"message": "System zarządzania transportem autobusowym"}