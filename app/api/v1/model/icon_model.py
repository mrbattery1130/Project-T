import os

from flask import current_app
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer


class Icon(Base):
    __tablename__ = "icon"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    _url: Column = Column("url", String(100), nullable=False)
    iconpack_id: Column = Column(Integer, nullable=False)
    app_id: Column = Column(Integer, nullable=False)
    progress = Column(String(100), nullable=True, default="nok")

    @property
    def url(self):
        site_domain = current_app.config.get(
            "SITE_DOMAIN",
            "http://{host}:{port}".format(
                host=current_app.config.get("FLASK_RUN_HOST", "127.0.0.1"),
                port=current_app.config.get("FLASK_RUN_PORT", "5000"),
            ),
        )

        if self._url is not None:
            return site_domain + os.path.join(
                current_app.static_url_path,
                # 'drawable/',
                self._url)
