from typing import List

from flask.json import jsonify
from lin.apidoc import api, DocResponse
from lin.redprint import Redprint

from app.exception.api import CatalogueNotFound
from app.model.icon_manager.app_model import App
from app.model.icon_manager.catalogue_model import Catalogue
from app.validator.schema import CatalogueOutSchema, BookSchemaList, CatalogueSchemaList

app_icon_api = Redprint('app_icon')


@app_icon_api.route('/app', methods=['GET'])
def get_apps():
    apps: List[App] = App.get_all_apps()
    return jsonify(apps)


@app_icon_api.route('/app', methods=['POST'])
def create_apps():
    pass
    # form = CreateOrUpdateAppForm().validate_for_api()
    # App.new_app(form)
    # return Success(msg='新建App成功')


# @icon_manager_api.route('/app_rel', methods=['POST'])
# def create_app_rel():
#     form = CreateOrUpdateBookForm().validate_for_api()
#     Book.new_book(form)
#     return Success(msg='新建图书成功')

@app_icon_api.route('/catalogue/<int:id>')
@api.validate(
    resp=DocResponse(CatalogueNotFound, r=CatalogueOutSchema),
    tags=['分类'],
)
def get_catalogue(id: int):
    c: Catalogue = Catalogue.get(id=id)
    if c:
        return c
    raise CatalogueNotFound


@app_icon_api.route("/catalogue")
@api.validate(
    resp=DocResponse(r=CatalogueSchemaList),
    tags=["分类"],
)
def get_catalogues():
    return Catalogue.get(one=False)
