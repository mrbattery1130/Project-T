from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer

from app.model.icon_manager.catalogue_model import Catalogue


class App(Base):
    __tablename__ = "app"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    name: Column = Column(String(50), nullable=False)
    name_en: Column = Column(String(50), nullable=False)
    catalogue_id: Column = Column(Integer, nullable=False)
    developer_name: Column = Column(String(50), nullable=True)
    description: Column = Column(String(1000), nullable=True)
    priority: Column = Column(Integer, default=999)

    @property
    def catalogue(self):
        return Catalogue.get(id=self.catalogue_id)
