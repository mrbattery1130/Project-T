from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer


class Icon(Base):
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    url: Column = Column(String(100), nullable=False)
    iconpack_id: Column = Column(Integer, nullable=False)
    app_id: Column = Column(Integer, nullable=False)
