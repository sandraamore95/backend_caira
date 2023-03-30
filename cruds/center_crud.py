import os
import shutil
from tkinter import E
from sqlalchemy.orm import Session
import schemas.center_schema as center_schema
import schemas.course_schema as course_schema
from fastapi import HTTPException
import models.center_model as center_model
from email_validator import validate_email, EmailNotValidError
from starlette import status


def my_validate_email(email: str):
    try:
        validate_email(email)
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email no es válido.",
        )


def get_center_by_email(db: Session, email: str):
    my_validate_email(email)
    return db.query(center_schema.Center).filter(center_schema.Center.email == email).first()


def get_center_by_id(db: Session, id: int):
    return db.query(center_schema.Center).filter(center_schema.Center.id == id).first()


def get_centers(db: Session, skip: int = 0):
    return db.query(center_schema.Center).offset(skip).all()


def add_center(db: Session, center: center_model.Center):
    center_image_path = "./public/center_images/" + str(center.email)
    if not os.path.exists(center_image_path):
        os.mkdir(center_image_path)
        os.mkdir(center_image_path + "/posts/")
        os.mkdir(center_image_path + "/courses/")

    new_center = center_schema.Center(
        name=center.name,
        email=center.email,
        type_center=center.type_center,
        acronym=center.acronym,
        location=center.location,
        url_web=center.url_web,
        contact=center.contact,
        telefono=center.telefono,
        description=center.description
    )

    db.add(new_center)
    db.flush()
    db.commit()
    db.refresh(new_center)
    return center_schema.Center(**center.dict())


def update_center(db: Session, email: str, details: center_model.CenterOptional):

    center = db.query(center_schema.Center).filter(
        center_schema.Center.email == email).first()
    center_exists = db.query(center_schema.Center).filter(
        center_schema.Center.email == details.email).first()

    details.id = center.id
    details.name = details.name if details.name != None else center.name
    details.email = center.email
    details.type_center = details.type_center if details.type_center != None else center.type_center
    details.acronym = details.acronym if details.acronym != None else center.acronym
    details.location = details.location if details.location != None else center.location
    details.url_web = details.url_web if details.url_web != None else center.url_web
    details.contact = details.contact if details.contact != None else center.contact
    details.telefono = details.telefono if details.telefono != None else center.telefono
    details.description = details.description if details.description != None else center.description

    if center_exists is None:
        old_center_images_path = "./public/center_images/" + str(center.email)
        new_center_images_path = "./public/center_images/" + str(details.email)
        shutil.move(old_center_images_path, new_center_images_path)
        if center.logo:
            logo_path = center.logo
            logo_path = logo_path.replace(center.email, details.email)
            details.logo = logo_path
        db.query(center_schema.Center).filter(
            center_schema.Center.email == email).update(vars(details))
        db.flush()
        db.commit()
        return db.query(center_schema.Center).filter(center_schema.Center.email == details.email).first()
    else:
        raise HTTPException(
            status_code=404, detail=f"El email al que intentas actualizar ya existe.")


def update_center_email(db: Session, email: str, details: center_model.CenterOptional):

    center = db.query(center_schema.Center).filter(
        center_schema.Center.email == email).first()
    center_exists = db.query(center_schema.Center).filter(
        center_schema.Center.email == details.email).first()

    details.id = center.id
    details.email = details.email if details.email != None else center.email
    details.name = center.name
    details.type_center = center.type_center
    details.acronym = center.acronym
    details.location = center.location
    details.url_web = center.url_web
    details.contact = center.contact
    details.telefono = center.telefono
    details.description = center.description

    if center_exists is None:
        old_center_images_path = "./public/center_images/" + str(center.email)
        new_center_images_path = "./public/center_images/" + str(details.email)
        shutil.move(old_center_images_path, new_center_images_path)
        if center.logo:
            logo_path = center.logo
            logo_path = logo_path.replace(center.email, details.email)
            details.logo = logo_path
        db.query(center_schema.Center).filter(
            center_schema.Center.email == email).update(vars(details))

    # CURSOS

        cursos = db.query(course_schema.Course).offset(0).all()

        for c in cursos:
            if c.center_id == center.id:
                if c.image is not None:
                    nuevopath = './public/center_images/' + \
                        details.email+'/courses/'+str(c.id)+'/image.png'

                    # actualizar el campo image
                    db.query(course_schema.Course).filter(course_schema.Course.id == c.id).update(
                        {
                            course_schema.Course.image: nuevopath
                        }
                    )

        db.flush()
        db.commit()
        return db.query(center_schema.Center).filter(center_schema.Center.email == details.email).first()
    else:
        raise HTTPException(
            status_code=404, detail=f"El email al que intentas actualizar ya existe.")


def delete_center(db: Session, email: str):
    try:
        db.query(center_schema.Center).filter(
            center_schema.Center.email == email).delete()
        db.commit()
        center_image_path = "./public/center_images/" + email
        shutil.rmtree(center_image_path, ignore_errors=True)
    except Exception as e:
        raise Exception(e)

# CATEGORIES #


def get_categories(db: Session, skip: int = 0):
    return db.query(center_schema.Categories).offset(skip).all()


def get_category_by_id(db: Session, id: int):
    return db.query(center_schema.Categories).filter(center_schema.Categories.id == id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(center_schema.Categories).filter(center_schema.Categories.name == name).first()


def add_category(db: Session, category: center_model.Categories):
    new_category = center_schema.Categories(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    return center_schema.Categories(**category.dict())


def delete_category(db: Session, id: int):
    try:
        db.query(center_schema.Categories).filter(
            center_schema.Categories.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)


def add_center_to_category(db: Session, data: center_model.Centers_Categories):
    new_data = center_schema.Centers_Categories(
        id_category=data.id_category,
        id_center=data.id_center
    )

    db.add(new_data)
    db.commit()
    return center_schema.Centers_Categories(**data.dict())


def get_centers_by_category(db: Session, id: int):
    categories = db.query(center_schema.Centers_Categories).filter(
        center_schema.Centers_Categories.id_category == id).all()
    centers = []
    if categories:
        for c in categories:
            center = db.query(center_schema.Center).filter(
                center_schema.Center.id == c.id_center).first()
            centers.append(center)
    return centers


def get_center_and_selected(db: Session, center: center_model.Center):

    course_first = db.query(course_schema.Course).filter(
        course_schema.Course.center_id == center.id).first()
    # si no encuentra ni el primer curso , esq no existen cursos en el centro
    if not course_first:

        # pero tiene que mostrar el centro igualmente
        return {
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
                "type_center": center.type_center
            }
        }
    # si tiene cursos podemos sacarlos :
    courses = db.query(course_schema.Course).filter(
        course_schema.Course.center_id == center.id, course_schema.Course.id != course_first.id).all()

    all_courses = []
    if courses:
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
                "id": course_first.id,
                "name": course_first.name,
                "category": course_first.category,
                "description": course_first.description,
                "image": course_first.image,
               
            },
            "other_courses":
            all_courses
        }}
    if all_info['center']['other_courses'] == []:
        del all_info['center']['other_courses']
    return all_info
