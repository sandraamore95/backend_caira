from db_handler import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Center(Base):
    __tablename__="centers"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True,nullable=False)
    name = Column(String(255),nullable=False)
    email = Column(String(255),unique=True,nullable=False)
    type_center = Column(String(255),nullable=False)
    acronym = Column(String(255))
    location = Column(String(255),nullable=False)
    url_web = Column(String(255))
    contact = Column(String(255))
    telefono=Column(String(255))
    logo = Column(String(255))
    description = Column(String(5000),nullable=False)

class Categories(Base):
    __tablename__="categories"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),unique=True,nullable=False)

class Centers_Categories(Base):
    __tablename__="centers_categories"
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    id_center = Column(Integer, ForeignKey("centers.id"),nullable=False)
    id_category = Column(Integer, ForeignKey("categories.id"), nullable=False)