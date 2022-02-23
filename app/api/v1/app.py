import math

from flask import Blueprint
from lin.apidoc import DocResponse
from lin.exception import Success
from lin.jwt import login_required
from sqlalchemy import text

from app.api.v1.exception import CatalogueNotFound, AppNotFound, AppRelNotFound

from app.api import AuthorizationBearerSecurity, api
from app.api.v1.model.app_model import App
from app.api.v1.model.app_rel_model import AppRel
from app.api.v1.model.catalogue_model import Catalogue
from app.api.v1.schema import *

app_api = Blueprint('app', __name__)


@app_api.route('/catalogue/<c_id>')
@api.validate(
    resp=DocResponse(CatalogueNotFound, r=CatalogueOutSchema),
    tags=['App'],
)
def get_catalogue(c_id: int):
    """
    获取id指定分类的信息
    """
    c: Catalogue = Catalogue.get(id=c_id)
    if c:
        return c
    raise CatalogueNotFound


@app_api.route("/catalogue")
@api.validate(
    resp=DocResponse(r=CatalogueSchemaList),
    tags=["App"],
)
def get_catalogues():
    """
    获取分类列表
    """
    return Catalogue.get(one=False)


@app_api.route('/<app_id>')
@api.validate(
    resp=DocResponse(AppNotFound, r=AppOutSchema),
    tags=['App'],
)
def get_app(app_id):
    """
    获取id指定App的信息
    """
    app: App = App.get(id=app_id)
    if app:
        app.catalogue = Catalogue.get(id=app.catalogue_id)
        app._fields.append("catalogue")

        app.app_rels = AppRel.get(app_id=app.id, one=False)
        app._fields.append("app_rels")
        return app
    raise AppNotFound


@app_api.route('')
@api.validate(
    # security=[AuthorizationBearerSecurity],
    query=AppQuerySearchSchema,
    resp=DocResponse(r=AppPageSchemaList),
    before=AppQuerySearchSchema.offset_handler,
    tags=["App"],
)
def get_apps():
    """
    获取App列表，分页展示
    """
    # return App.get(one=False)
    apps = App.query.filter()
    total = apps.count()
    items = (
        apps.order_by(text("create_time desc")).offset(g.offset).limit(g.count).all()
    )
    for app in items:
        app.catalogue = Catalogue.get(id=app.catalogue_id)
        app._fields.append("catalogue")

        app.app_rels: List[AppRel] = AppRel.get(app_id=app.id, one=False)
        app._fields.append("app_rels")

        pn = []
        for a in app.app_rels:
            pn.append(a.package_name)
        app.package_names = list(set(pn))
        app._fields.append("package_names")

    total_page = math.ceil(total / g.count)

    return AppPageSchemaList(
        page=g.page,
        count=g.count,
        total=total,
        items=items,
        total_page=total_page,
    )


@app_api.route("", methods=["POST"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(16)),
    tags=["App"],
)
def create_app(json: AppInSchema):
    """
    创建App
    """
    App.create(**json.dict(), commit=True)
    return Success(16)


@app_api.route("/<app_id>", methods=["PUT"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(17)),
    tags=["App"],
)
def update_app(app_id, json: AppInSchema):
    """
    更新App信息
    """
    app = App.get(id=app_id)
    if app:
        app.update(
            id=app_id,
            **json.dict(),
            commit=True,
        )
        return Success(17)
    raise AppNotFound


@app_api.route("/<app_id>", methods=["DELETE"])
# @permission_meta(name="删除App", module="App")
# @group_required
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(AppNotFound, Success(18)),
    tags=["App"],
)
def delete_app(app_id):
    """
    传入id删除对应App
    """
    app = App.get(id=app_id)
    if app:
        # 删除App，软删除
        app.delete(commit=True)
        return Success(18)
    raise AppNotFound


@app_api.route('/app_rel/<app_rel_id>')
@api.validate(
    resp=DocResponse(r=AppRelSchemaList),
    tags=['App'],
)
def get_app_rel(app_rel_id):
    """
    获取id指定App发行版的信息
    """
    return AppRel.get(id=app_rel_id, one=True)


@app_api.route('/app_rels_by_app/<app_id>')
@api.validate(
    resp=DocResponse(r=AppRelSchemaList),
    tags=['App'],
)
def get_app_rels_by_app(app_id):
    """
    获取id指定App下所有发行版的信息
    """
    return AppRel.get(app_id=app_id, one=False)


@app_api.route("/app_rel", methods=["POST"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(19)),
    tags=["App"],
)
def create_app_rel(json: AppRelInSchema):
    """
    创建App发行版
    """
    AppRel.create(**json.dict(), commit=True)
    return Success(19)


@app_api.route("/app_rel/<app_rel_id>", methods=["PUT"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(20)),
    tags=["App"],
)
def update_app_rel(app_rel_id, json: AppRelInSchema):
    """
    更新App发行版信息
    """
    app_rel = App.get(id=app_rel_id)
    if app_rel:
        app_rel.update(
            id=app_rel_id,
            **json.dict(),
            commit=True,
        )
        return Success(20)
    raise AppRelNotFound


@app_api.route("/app_rel/<app_rel_id>", methods=["DELETE"])
# @permission_meta(name="删除App发行版", module="App")
# @group_required
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(AppNotFound, Success(21)),
    tags=["App"],
)
def delete_app_rel(app_rel_id):
    """
    传入id删除对应App发行版
    """
    app_rel = AppRel.get(id=app_rel_id)
    if app_rel:
        # 删除App，软删除
        app_rel.delete(commit=True)
        return Success(21)
    raise AppRelNotFound
