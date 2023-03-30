import os
from fastapi import Depends, File, HTTPException, APIRouter, UploadFile
from sqlalchemy.orm import Session
from typing import List
import cruds.center_crud as center_crud
import schemas.center_schema as center_schema
import models.center_model as center_model
from db_handler import SessionLocal, engine
from fastapi.responses import FileResponse

center_schema.Base.metadata.create_all(bind=engine)

center = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@center.get('/all_centers',response_model=List[center_model.Center])
def all_centers(skip: int = 0, db: Session = Depends(get_db)):
    centers = center_crud.get_centers(db=db, skip=skip)
    return centers

@center.get('/get_center/{email}')
def get_center(email: str, db: Session = Depends(get_db)):
    center = center_crud.get_center_by_email(db=db, email=email)
    if not center:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el centro")
    return center

@center.post('/add_center',response_model=center_model.Center)
def add_center(center: center_model.Center, db: Session = Depends(get_db)):
    center_email = center_crud.get_center_by_email(db=db, email=center.email)
    if center_email:
        raise HTTPException(status_code=400, detail=f"Centro {center.email} ya existe.")
        
    return center_crud.add_center(db=db, center=center)

@center.put('/update_center/{email}', response_model=center_model.Center)
def update_center(email: str, update_param: center_model.CenterOptional, db: Session = Depends(get_db)):

    details = center_crud.get_center_by_email(db=db, email=email)

    if not details:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el centro")
    
    return center_crud.update_center(db=db, details=update_param, email=email)

@center.delete('/delete_center/{email}')
def delete_center(email: str, db: Session = Depends(get_db)):
    
    details = center_crud.get_center_by_email(db=db, email=email)
    
    if not details:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el centro")

    try:
        center_crud.delete_center(db=db, email=email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fallo al eliminar: {e}")
    return {"Delete status": "success"}

#Sirve para update
@center.post('/add_center_logo/{email}')
async def add_center_logo(email: str, file: UploadFile = File(...), db: Session= Depends(get_db)):
    center = center_crud.get_center_by_email(db=db, email=email)
    if not center:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el email")
    allowedFiles = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type in allowedFiles:
        center_image_path = "./public/center_images/" + center.email + "/logo.png"
        with open(center_image_path , "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            buffer.close()
            db.query(center_schema.Center).filter(center_schema.Center.email == email).update({"logo": center_image_path})
            db.commit()
            return file.filename
    else:
        raise HTTPException(status_code=404, detail=f"El formato del archivo no es correcto.")

@center.get("/get_center_logo/{email}")
async def get_center_logo(email: str, db: Session= Depends(get_db)):
    center = center_crud.get_center_by_email(db=db, email=email)
    if center:
        if center.logo is not None:
            return FileResponse(center.logo) if os.path.exists(center.logo) else ''
        else:
            return ''
    else:
        raise HTTPException(status_code=400, detail=f"El centro no existe.")


@center.put('/update_email_center/{email}', response_model=center_model.Center)
def update_center_email(email: str, update_param: center_model.CenterOptional, db: Session = Depends(get_db)):

    details = center_crud.get_center_by_email(db=db, email=email)

    if not details:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el centro")
    
    return center_crud.update_center_email(db=db, details=update_param, email=email)

# CATEGORIES #

@center.get('/all_categories',response_model=List[center_model.Categories])
def all_categories(skip: int = 0, db: Session = Depends(get_db)):
    categories = center_crud.get_categories(db=db, skip=skip)
    return categories

@center.get('/get_category/{id}')
def get_category(id: int, db: Session = Depends(get_db)):
    category = center_crud.get_category_by_id(db=db, id=id)
    if not category:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado la categoría")
    return category

@center.post('/add_category',response_model=center_model.Categories)
def add_category(category: center_model.Categories, db: Session = Depends(get_db)):
    category_name = center_crud.get_category_by_name(db=db, name=category.name)
    if category_name:
        raise HTTPException(status_code=400, detail=f"Categoría {category.name} ya existe.")

    return center_crud.add_category(db=db, category=category)

@center.delete('/delete_category/{id}')
def delete_category(id: int, db: Session = Depends(get_db)):
    
    details = center_crud.get_category_by_id(db=db, id=id)
    
    if not details:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado la categoría")

    try:
        center_crud.delete_category(db=db, id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fallo al eliminar: {e}")
    return {"Delete status": "success"}

@center.post('/add_center_to_category',response_model=center_model.Centers_Categories)
def add_center_to_category(data: center_model.Centers_Categories, db: Session = Depends(get_db)):
    category = center_crud.get_category_by_id(db=db, id=data.id_category)
    center = center_crud.get_center_by_id(db=db, id=data.id_center)
    if not category:
        raise HTTPException(status_code=400, detail=f"Categoría {data.id_category} no existe.")
    if not center:
        raise HTTPException(status_code=400, detail=f"Centro {data.id_center} no existe.")
    return center_crud.add_center_to_category(db=db, data=data)

@center.get('/get_centers_by_category/{id}')
def get_centers_by_category(id: int, db: Session = Depends(get_db)):
    category = center_crud.get_category_by_id(db=db, id=id)
    if not category:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado la categoría")
    else:
        return center_crud.get_centers_by_category(db=db, id=id)

@center.get('/highlight_center/{center_id}')
def highlight_center(center_id: int, db: Session = Depends(get_db)):
    center = center_crud.get_center_by_id(db=db, id=center_id)
    if not center:
        raise HTTPException(
            status_code=400, detail=f"No existe ningún centro con este ID")
    return center_crud.get_center_and_selected(db=db, center=center)