from pydantic import BaseModel, ConfigDict
from typing import Optional

class CourseBase(BaseModel):
    name: str
    code: str
    units: float
    grade: Optional[str] = None
    semester: str

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    units: Optional[float] = None
    grade: Optional[str] = None
    semester: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)