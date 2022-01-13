from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer


class AppRel(Base):
    __tablename__ = "app_rel"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    package_name: Column = Column(String(100), nullable=False)
    launch_name: Column = Column(String(500), nullable=True)
    app_id: Column = Column(Integer, autoincrement=True)