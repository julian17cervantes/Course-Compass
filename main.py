# Python, venv, fastapi, uvicorn
# PostgreSQL, SQLAlchemy
# Pydantic models
# Pytest
# Auth (JWT + bcrypy)
# Docker + Railway + Github Actions

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Cource Compass is alive"}

from database import engine
from models import Base

Base.metadata.create_all(bind=engine)