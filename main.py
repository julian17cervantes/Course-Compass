from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from gpa import calculate_gpa
from models import Base, Course, User
from schemas import CourseCreate, CourseRead, CourseUpdate, Token, UserCreate, UserRead
from auth import create_access_token, hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm

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

@app.get("/courses", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: int, updates: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()

@app.get("/gpa")
def get_gpa(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    cumulative = calculate_gpa([(c.grade, c.units) for c in courses])

    by_semester = {}
    for c in courses:
        by_semester.setdefault(c.semester, []).append((c.grade, c.units))
    return {
        "cumulative_gpa": cumulative,
        "by_semester": {
            semester: calculate_gpa(pairs)
            for semester, pairs in by_semester.items()
        },
    }

@app.post("/signup", response_model=UserRead, status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email alreadly registered")
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if db_user is None or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_access_token(db_user.email), "token_type": "bearer"}