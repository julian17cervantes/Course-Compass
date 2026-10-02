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