from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.database import engine, SQLModel
from app.routers import users, login, academic

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(academic.router)

