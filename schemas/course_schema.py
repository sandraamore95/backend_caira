from db_handler import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL

class Course(Base):
    __tablename__="courses"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True,nullable=False)
    name = Column(String(255),nullable=False)
    category = Column(String(255),nullable=False)
    description = Column(String(1000),nullable=False)
    center_id = Column(Integer, ForeignKey("centers.id"),nullable=False)
    image = Column(String(255))
   
class Course_Especifications(Base):
    __tablename__="course_especifications"
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    id_course = Column(Integer, ForeignKey("courses.id"),nullable=False)
    modality = Column(String(255),nullable=False)
    language = Column(String(255),nullable=False)
    price = Column(DECIMAL,nullable=False)
    duration = Column(String(255),nullable=False)
    vacancies = Column(Integer)
    scholarship = Column(String(255))
    location = Column(String(255),nullable=False)
    
    
   