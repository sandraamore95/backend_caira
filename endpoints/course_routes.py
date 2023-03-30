from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import cruds.course_crud as course_crud
import schemas.course_schema as course_schema
import schemas.center_schema as center_schema
import models.course_model as course_model
from db_handler import SessionLocal, engine
import shutil
import os

course_schema.Base.metadata.create_all(bind=engine)

course = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Coger todos los cursos de todos los centros


@course.get('/all_courses')
def all_courses(skip: int = 0, db: Session = Depends(get_db)):
    courses = course_crud.get_all_courses(db=db, skip=skip)
    if not courses:
        raise HTTPException(
            status_code=400, detail=f"No se ha encontrado la respuesta")
    return courses


@course.get('/get_course/{id}')
def get_course(id: int, db: Session = Depends(get_db)):
    center = course_crud.get_course_by_id(db=db, id=id)
    if not center:
        raise HTTPException(status_code=400, detail=f"No se ha encontrado el curso")
    return center


@course.get('/get_courses_centers/{center_id}')
def get_courses(center_id: int, db: Session = Depends(get_db)):
    center = course_crud.get_courses_by_id(db=db, id=center_id)
    if not center:
        raise HTTPException(
            status_code=400, detail=f"El centro no existe o no tiene cursos")
    return center

# Coger todos los cursos de una categoría


@course.get('/get_courses_by_category/{category}')
def get_courses(category: str, db: Session = Depends(get_db)):
    center = course_crud.get_courses_by_category(db=db, category=category)
    if not center:
        raise HTTPException(
            status_code=400, detail=f"No hay ningún curso con ésta categoría")
    return center


@course.post('/add_course', response_model=course_model.Course)
async def add_course(course: course_model.Course = Depends(), file: UploadFile or None = None, db: Session = Depends(get_db)):
    center_exists = db.query(center_schema.Center).filter(
        center_schema.Center.id == course.center_id).first()
    if not center_exists:
        raise HTTPException(status_code=400, detail=f"Centro no existe.")
    else:
        posts = course_crud.add_course(db=db, post=course)
        if file:
            await course_crud.add_image_course(db=db, file=file, course_exists=posts, center=center_exists)
        db.commit()
    return course_crud.add_course(db=db, post=course)


@course.post('/add_course_logo/{id}')
async def add_course_logo(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    course = course_crud.get_course_by_id(db=db, id=id)
    if not course:
        raise HTTPException(
            status_code=400, detail=f"No se ha encontrado el curso ")
    allowedFiles = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type in allowedFiles:
        email_center = course['center']['email']
        course_image_path = "./public/center_images/" + \
            email_center + "/courses/" + str(id)
        if not os.path.exists(course_image_path):
            os.mkdir(course_image_path)
        course_image_path = "./public/center_images/" + \
            email_center + "/courses/" + str(id) + '/image.png'
        with open(course_image_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            buffer.close()
            db.query(course_schema.Course).filter(
                course_schema.Course.id == id).update({"image": course_image_path})
            db.commit()
            return file.filename
    else:
        raise HTTPException(
            status_code=404, detail=f"El formato del archivo no es correcto.")


@course.get("/get_course_logo/{id}")
async def get_course_logo(id: int, db: Session = Depends(get_db)):
    course = course_crud.get_course_id(db=db, id=id)
    
    if course:
        if course.image is not None:
            return FileResponse(course.image) if os.path.exists(course.image) else ''
        else:
            return ''
    else:
        raise HTTPException(status_code=400, detail=f"El curso no existe.")


@course.put('/update_course/{id}', response_model=course_model.Course)
def update_course(id: int, update_param: course_model.CourseOptional, db: Session = Depends(get_db)):

    details = course_crud.get_course_by_id(db=db, id=id)

    if not details:
        raise HTTPException(
            status_code=400, detail=f"No se ha encontrado el curso")

    return course_crud.update_course(db=db, details=update_param, id=id)


@course.delete('/delete_course/{id}')
def delete_course(id: int, db: Session = Depends(get_db)):

    details = course_crud.get_course_id(db=db, id=id)

    if not details:
        raise HTTPException(
            status_code=400, detail=f"No se ha encontrado el curso")

    try:
        course_crud.delete_course(db=db, id=id)
        # recogemos el email del diccionario para ponerlo en la ruta
        email_center = details['center']['email']
        course_image_path = "./public/center_images/" + \
            email_center + "/courses/" + str(id)
        shutil.rmtree(course_image_path, ignore_errors=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fallo al eliminar: {e}")
    return {"Delete status": "success"}


@course.get('/highlight_center_course/{course_id}')
def highlight_center_course(course_id: int, db: Session = Depends(get_db)):
    return course_crud.get_courses_and_selected(db=db, course_id=course_id)


# especificaciones curso

@course.post('/add_course_especification_tocourse')
async def add_course_especification(course_especification: course_model.Course_Especifications = Depends(), db: Session = Depends(get_db)):
    
    course = course_crud.get_course_by_id(db=db, id=course_especification.id_course)
    if not course:
        raise HTTPException(status_code=400, detail=f"Curso no existe.")
    else:
        return course_crud.add_course_especification(db=db, post=course_especification)


@course.get('/get_especification_ofcourse/{course_id}')
def get_courses_especification(course_id: int, db: Session = Depends(get_db)):
    course_espec = course_crud.get_course_espec_by_id(db=db, id=course_id)
    if not course_espec:
        raise HTTPException(
            status_code=400, detail=f"No se han encontrado especificaciones para el curso!")
    return course_espec
