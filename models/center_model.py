from pydantic import BaseModel, validator
from typing import Optional
from fastapi import HTTPException

class Center(BaseModel):
    id : Optional[int]
    name: str
    email: str
    type_center: str
    acronym: str
    location: str
    url_web: Optional[str]
    contact : Optional[str]
    telefono : Optional[str]
    logo: Optional[str]
    description : str
    
    class Config:
        orm_mode = True
    
    
    @validator('name')
    def validate_name(cls, v):
        for lett in v:  
            if not ( v[0].isnumeric() or v[0].isupper()):
                raise HTTPException(status_code=400, detail="El nombre debe empezar por mayúscula")
        return v
  
class CenterOptional(Center):
    __annotations__ = {k: Optional[v] for k, v in Center.__annotations__.items()}
    
class Categories(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True

    @validator('name')
    def validate_name(cls, v):
        for lett in v:
            if not (lett.isalpha() or lett.isspace()):
                if lett == "/":
                    continue
                else:
                    raise HTTPException(status_code=400, detail="La categoría solo puede contener letras")
        if not v[0].isupper():
            raise HTTPException(status_code=400, detail="La categoría debe empezar por mayúscula")
        
        return v

class Centers_Categories(BaseModel):
    id: Optional[int]
    id_center: int
    id_category: int
    
    class Config:
        orm_mode = True
