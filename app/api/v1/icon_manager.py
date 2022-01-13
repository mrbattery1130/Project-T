import math

from flask import request, g
from lin import permission_meta
from lin.apidoc import api, DocResponse
from lin.exception import Success
from lin.jwt import login_required, group_required
from lin.redprint import Redprint
from sqlalchemy import text

from app.exception.api import CatalogueNotFound, AppNotFound
from app.model.icon_manager.app_model import App
from app.model.icon_manager.catalogue_model import Catalogue
from app.validator.schema import CatalogueOutSchema, CatalogueSchemaList, AppOutSchema, AuthorizationSchema, \
    AppInSchema, AppPageSchemaList

app_icon_api = Redprint('app_icon')


@app_icon_api.route('/catalogue/<c_id>')
@api.validate(
    resp=DocResponse(CatalogueNotFound, r=CatalogueOutSchema),
    tags=['分类'],
)
def get_catalogue(c_id: int):
    c: Catalogue = Catalogue.get(id=c_id)
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


@app_icon_api.route('/app/<app_id>')
@api.validate(
    resp=DocResponse(AppNotFound, r=AppOutSchema),
    tags=['App'],
)
def get_app(app_id):
    app: App = App.get(id=app_id)
    if app:
        return app
    raise AppNotFound


@app_icon_api.route('/app')
@api.validate(
    resp=DocResponse(r=AppPageSchemaList),
    tags=["App"],
)
def get_apps():
    # return App.get(one=False)
    apps = App.query.filter()
    total = apps.count()
    items = (
        apps.order_by(text("create_time desc")).offset(g.offset).limit(g.count).all()
    )
    total_page = math.ceil(total / g.count)

    return App.get(
        page=g.page,
        count=g.count,
        total=total,
        items=items,
        total_page=total_page,
    )


@app_icon_api.route("", methods=["POST"])
@login_required
@api.validate(
    headers=AuthorizationSchema,
    json=AppInSchema,
    resp=DocResponse(Success(16)),
    tags=["App"],
)
def create_app():
    app_schema = request.context.json
    App.create(**app_schema.dict(), commit=True)
    return Success(16)


@app_icon_api.route("/<app_id>", methods=["PUT"])
@login_required
@api.validate(
    headers=AuthorizationSchema,
    json=AppInSchema,
    resp=DocResponse(Success(17)),
    tags=["App"],
)
def update_app(app_id):
    """
    更新图书信息
    """
    app_schema = request.context.json
    app = App.get(id=app_id)
    if app:
        app.update(
            id=app_id,
            **app_schema.dict(),
            commit=True,
        )
        return Success(17)
    raise AppNotFound


@app_icon_api.route("/<app_id>", methods=["DELETE"])
# @permission_meta(name="删除App", module="App")
# @group_required
@login_required
@api.validate(
    headers=AuthorizationSchema,
    resp=DocResponse(AppNotFound, Success(18)),
    tags=["App"],
)
def delete_book(app_id):
    """
    传入id删除对应图书
    """
    app = App.get(id=app_id)
    if app:
        # 删除App，软删除
        app.delete(commit=True)
        return Success(18)
    raise AppNotFound
