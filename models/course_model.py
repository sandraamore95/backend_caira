from decimal import Decimal
from pydantic import BaseModel, validator
from typing import Optional
from fastapi import HTTPException


class Course(BaseModel):
    id: Optional[int]
    name: str
    category: str
    center_id: int
    description: str
    image: Optional[str]

    class Config:
        orm_mode = True

    @validator('name')
    def validate_name(cls, v):
        for lett in v:
            if not (lett.isalpha() or lett.isspace()):
                raise HTTPException(
                    status_code=400, detail="El nombre solo puede contener letras")
        if not v[0].isupper():
            raise HTTPException(
                status_code=400, detail="El nombre debe empezar por mayúscula")

        return v


class CourseOptional(Course):
    __annotations__ = {k: Optional[v]
                       for k, v in Course.__annotations__.items()}


class Course_Especifications(BaseModel):
    id: Optional[int]
    id_course: int
    modality: str
    language: str
    price: int
    duration: str
    vacancies: Optional[int]
    scholarship: Optional[str]
    location: str

    class Config:
        orm_mode = True
