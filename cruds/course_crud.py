from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import schemas.course_schema as course_schema
import schemas.center_schema as center_schema
import models.course_model as course_model
import os


def get_course_id(db: Session, id: int):
    course = db.query(course_schema.Course).filter(
        course_schema.Course.id == id).first()
    return course

def get_course_by_id(db: Session, id: int):
    course = db.query(course_schema.Course).filter(
        course_schema.Course.id == id).first()
    if course:
        # el curso existe !
        center = db.query(center_schema.Center).filter(
            center_schema.Center.id == course.center_id).first()
        especification = db.query(course_schema.Course_Especifications).filter(
            course_schema.Course_Especifications.id_course == course.id).all()

        all_courses = []
        course = {
            "id": course.id,
            "name": course.name,
            "category": course.category,
            "description": course.description,
            "image": course.image,
            "center": {
                "id": course.center_id,
                "acronym": center.acronym,
                "type_center": center.type_center,
                "name": center.name,
                "email": center.email,
                "location": center.location,
                "logo": center.logo,
                "description": center.description,
                "website": center.url_web,
                "contact": center.contact,
                "telefono": center.telefono
            }

        }
        all_courses.append(course)
        for ce in especification:

            course_espec = {
                "id": ce.id,
                "modality": ce.modality,
                "price": ce.price,
                "language": ce.language,
                "duration": ce.duration,
                "vacancies": ce.vacancies,
                "location": ce.location,
                "scholarship": ce.scholarship

            }
            all_courses.append(course_espec)
        return all_courses


def get_course_espec_by_id(db: Session, id: int):
    course = db.query(course_schema.Course_Especifications).filter(
        course_schema.Course_Especifications.id_course == id).all()
    return course


def get_courses_by_category(db: Session, category: str):
    courses = db.query(course_schema.Course).filter(
        course_schema.Course.category == category).all()
    all_courses = []
    if courses:
        for c in courses:
            center = db.query(center_schema.Center).filter(
                center_schema.Center.id == c.center_id).first()
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).first()
            course = {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "description": c.description,
                "image": c.image,
                "center": {
                    "id": c.center_id,
                    "acronym": center.acronym,
                    "type_center": center.type_center,
                    "name": center.name,
                    "email": center.email,
                    "location": center.location,
                    "logo": center.logo,
                    "description": center.description,
                    "website": center.url_web,
                    "contact": center.contact,
                    "telefono": center.telefono,
                }
            }
            all_courses.append(course)
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).all()
            for ce in especification:
                course_espec = {
                    "id_especification": ce.id,
                    "modality": ce.modality,
                    "price": ce.price,
                    "language": ce.language,
                    "duration": ce.duration,
                    "vacancies": ce.vacancies,
                    "location": ce.location,
                    "scholarship": ce.scholarship
                }
                all_courses.append(course_espec)

            
        return all_courses


def get_courses_by_id(db: Session, id: int):
    courses = db.query(course_schema.Course).filter(
        course_schema.Course.center_id == id).all()
    all_courses = []
    if courses:
        for c in courses:
            center = db.query(center_schema.Center).filter(
                center_schema.Center.id == c.center_id).first()
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).first()
            course = {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "description": c.description,
                "image": c.image,
                "center": {
                    "id": c.center_id,
                    "acronym": center.acronym,
                    "type_center": center.type_center,
                    "name": center.name,
                    "email": center.email,
                    "location": center.location,
                    "logo": center.logo,
                    "description": center.description,
                    "website": center.url_web,
                    "contact": center.contact,
                    "telefono": center.telefono,
                }
            }
            all_courses.append(course)
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).all()
            for ce in especification:
                course_espec = {
                    "id_especification": ce.id,
                    "modality": ce.modality,
                    "price": ce.price,
                    "language": ce.language,
                    "duration": ce.duration,
                    "vacancies": ce.vacancies,
                    "location": ce.location,
                    "scholarship": ce.scholarship
                }
                all_courses.append(course_espec)

            
        return all_courses


def get_all_courses(db: Session, skip: int = 0):
    courses = db.query(course_schema.Course).offset(skip).all()
    all_courses = []
    if courses:
        for c in courses:
            center = db.query(center_schema.Center).filter(
                center_schema.Center.id == c.center_id).first()
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).first()
            course = {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "description": c.description,
                "image": c.image,
                "center": {
                    "id": c.center_id,
                    "acronym": center.acronym,
                    "type_center": center.type_center,
                    "name": center.name,
                    "email": center.email,
                    "location": center.location,
                    "logo": center.logo,
                    "description": center.description,
                    "website": center.url_web,
                    "contact": center.contact,
                    "telefono": center.telefono,
                }
            }
            all_courses.append(course)
            especification = db.query(course_schema.Course_Especifications).filter(
                course_schema.Course_Especifications.id_course == c.id).all()
            for ce in especification:
                course_espec = {
                    "id_especification": ce.id,
                    "modality": ce.modality,
                    "price": ce.price,
                    "language": ce.language,
                    "duration": ce.duration,
                    "vacancies": ce.vacancies,
                    "location": ce.location,
                    "scholarship": ce.scholarship
                }
                all_courses.append(course_espec)

            
        return all_courses


async def add_image_course(db: Session, file: UploadFile or None, course_exists=course_schema.Course, center=center_schema.Center):
    if file:
        allowedFiles = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if file.content_type in allowedFiles:
            db.flush()
            course_multimedia_path = "./public/center_images/" + \
                str(center.email)
            center_course_path = course_multimedia_path + "/courses/"
            course_id_multimedia_path = center_course_path + \
                str(course_exists.id)
            course_id_file_multimedia_path = course_id_multimedia_path + "/image.png"
            if not os.path.exists(course_multimedia_path):
                os.mkdir(course_multimedia_path)
            if not os.path.exists(center_course_path):
                os.mkdir(center_course_path)
            if not os.path.exists(course_id_multimedia_path):
                os.mkdir(course_id_multimedia_path)

            with open(course_id_file_multimedia_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                buffer.close()
                course_exists.image = course_id_file_multimedia_path
        else:
            raise HTTPException(
                status_code=404, detail=f"El formato del archivo no es válido.")
        return course_exists
    else:
        raise HTTPException(
            status_code=404, detail=f"No se ha pasado ningún archivo.")


def add_course(db: Session, post: course_model.Course):
    new_course = course_schema.Course(
        name=post.name,
        category=post.category,
        center_id=post.center_id,
        description=post.description,
    )
    db.add(new_course)
    return new_course


def update_course(db: Session, id: int, details: course_model.CourseOptional):

    course = db.query(course_schema.Course).filter(
        course_schema.Course.id == id).first()
    details.id = course.id
    details.name = details.name if details.name != None else course.name
    details.category = details.category if details.category != None else course.category
    details.center_id = course.center_id
    details.description = details.description if details.description != None else course.description
    details.image = course.image

    db.query(course_schema.Course).filter(
        course_schema.Course.id == id).update(vars(details))
    db.commit()
    return db.query(course_schema.Course).filter(course_schema.Course.id == id).first()


def get_courses_and_selected(db: Session, course_id: int):

    course_selected = db.query(course_schema.Course).filter(
        course_schema.Course.id == course_id).first()

    if not course_selected:
        raise HTTPException(
            status_code=400, detail=f"No existe ningún curso con este ID")
    else:
        center = db.query(center_schema.Center).filter(
            center_schema.Center.id == course_selected.center_id).first()
        courses = db.query(course_schema.Course).filter(
            course_schema.Course.center_id == center.id, course_schema.Course.id != course_selected.id).all()
    all_courses = []
    if course_selected and center:
        for c in courses:
            course = {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "description": c.description,
                "image": c.image,
            }
            all_courses.append(course)
    
    all_info = {
        "center": {
            "id": center.id,
            "name": center.name,
            "email": center.email,
            "location": center.location,
            "acronym": center.acronym,
            "logo": center.logo,
            "description": center.description,
            "website": center.url_web,
            "contact": center.contact,
            "telefono": center.telefono,
            "type_center": center.type_center,
            "course_selected": {
                "id": course_selected.id,
                "name": course_selected.name,
                "category": course_selected.category,
                "description": course_selected.description,
                "image": course_selected.image,
            },
            "other_courses":
                all_courses
        }}
    if all_info['center']['other_courses'] == []:
        del all_info['center']['other_courses']

    return all_info


def delete_course(db: Session, id: int):
    try:
        db.query(course_schema.Course).filter(
            course_schema.Course.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)

# especificaaciones curso


def add_course_especification(db: Session, post: course_model.Course_Especifications):
    course_especification = course_schema.Course_Especifications(

        modality=post.modality,
        language=post.language,
        price=post.price,
        duration=post.duration,
        id_course=post.id_course,
        vacancies=post.vacancies,
        scholarship=post.scholarship,
        location=post.location,

    )
    db.add(course_especification)
    db.flush()
    db.commit()
    db.refresh(course_especification)
    return course_especification
