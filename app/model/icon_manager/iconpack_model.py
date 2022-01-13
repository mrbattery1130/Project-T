from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer


class Iconpack(Base):
    __tablename__ = "iconpack"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    name: Column = Column(String(50), nullable=False)
    description: Column = Column(String(1000), nullable=True)
