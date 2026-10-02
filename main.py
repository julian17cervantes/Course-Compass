from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Course
from schemas import CourseCreate, CourseRead

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Cource Compass is alive"}

@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course