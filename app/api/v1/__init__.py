from flask import Blueprint

from app.api.v1 import book, app, icon_util, icon, iconpack


def create_v1():
    bp_v1 = Blueprint("v1", __name__)
    from app.api.v1.book import book_api
    from app.api.v1.app import app_api
    # from app.api.v1.icon_util import icon_util_api
    from app.api.v1.icon import icon_api
    from app.api.v1.iconpack import iconpack_api

    bp_v1.register_blueprint(book_api, url_prefix="/book")
    bp_v1.register_blueprint(app_api, url_prefix="/app")
    # bp_v1.register_blueprint(icon_util_api, url_prefix="/icon_util")
    bp_v1.register_blueprint(icon_api, url_prefix="/icon")
    bp_v1.register_blueprint(iconpack_api, url_prefix="/iconpack")

    return bp_v1
