from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer


class Catalogue(Base):
    __tablename__ = "catalogue"
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String(100), nullable=False)
    name_en: Column = Column(String(100), nullable=False)
