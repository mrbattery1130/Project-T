from typing import List

from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer

from app.api.v1.model.app_rel_model import AppRel
from app.api.v1.model.catalogue_model import Catalogue


class App(Base):
    __tablename__ = "app"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    name: Column = Column(String(50), nullable=False)
    name_en: Column = Column(String(50), nullable=False)
    catalogue_id: Column = Column(Integer, nullable=False)
    developer_name: Column = Column(String(50), nullable=True)
    description: Column = Column(String(1000), nullable=True)
    priority: Column = Column(Integer, default=999)

    @classmethod
    def get(cls, start=None, count=None, one=True, **kwargs):
        app = super(App, cls).get(start=start, count=count, one=one, **kwargs)
        app.append_attrs()
        return app

    def append_attrs(self):
        self.catalogue = Catalogue.get(id=self.catalogue_id)
        self._fields.append("catalogue")

        app_rels: List[AppRel] = AppRel.get(app_id=self.id, one=False)
        pn = []
        for a in app_rels:
            pn.append(a.package_name)
        self.package_names = list(set(pn))
        self._fields.append("package_names")
