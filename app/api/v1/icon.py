import math

from flask import Blueprint, g
from lin.apidoc import DocResponse
from lin.exception import Success
from lin.jwt import login_required
from sqlalchemy import or_

from app.api import api, AuthorizationBearerSecurity
from app.api.v1.exception import IconNotFound, IconCannotReopen
from app.api.v1.model.app_model import App
from app.api.v1.model.icon_model import Icon
from app.api.v1.schema import IconOutSchema, IconInSchema, IconQuerySearchSchema, \
    IconPageSchemaList

icon_api = Blueprint('icon', __name__)


@icon_api.route('/<icon_id>')
@api.validate(
    resp=DocResponse(IconNotFound, r=IconOutSchema),
    tags=["图标"],
)
def get_icon(icon_id):
    """
    获取id指定图标的信息
    """
    icon: Icon = Icon.get(id=icon_id)
    if icon:
        return icon
    raise IconNotFound


@icon_api.route('')
@api.validate(
    query=IconQuerySearchSchema,
    resp=DocResponse(r=IconPageSchemaList),
    before=IconQuerySearchSchema.offset_handler,
    tags=["图标"],
)
def get_icons():
    """
    获取图标列表，分页展示
    """
    # return Icon.get(one=False)
    icons = Icon.query.filter(Icon.is_deleted == False)
    # filter
    if g.app_id:
        icons = icons.filter(Icon.app_id == g.app_id)
    if g.iconpack_id:
        icons = icons.filter(Icon.iconpack_id == g.iconpack_id)
    if g.keyword:
        # 查询图标对应App的名称、英文名中包含keyword的项
        icons = icons.join(App, Icon.app_id == App.id).filter(
            or_(App.name.like("%" + g.keyword + "%"),
                App.name_en.like("%" + g.keyword + "%")),
            App.is_deleted == False
        )
    if g.catalogue_id:
        # 查询图标对应App的分类
        icons = icons.join(App, Icon.app_id == App.id) \
            .filter(App.catalogue_id == g.catalogue_id, App.is_deleted == False)
    if g.progess:
        icons = icons.filter(Icon.progress == g.progess)
    # order
    if g.order_by == "id":
        icons = icons.order_by(Icon.id)
    elif g.order_by == "id_desc":
        icons = icons.order_by(Icon.id.desc())
    elif g.order_by == "create_time":
        icons = icons.order_by(Icon.create_time)
    else:
        icons = icons.order_by(Icon.create_time.desc())

    total = icons.count()
    items = icons.offset(g.offset).limit(g.count).all()
    for icon in items:
        icon.app = App.get(id=icon.app_id, one=True)
        icon._fields.append("app")

    total_page = math.ceil(total / g.count)
    return IconPageSchemaList(
        page=g.page,
        count=g.count,
        total=total,
        items=items,
        total_page=total_page,
    )


@icon_api.route("", methods=["POST"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(22)),
    tags=["图标"],
)
def create_icon(json: IconInSchema):
    """
    创建图标
    """
    Icon.create(**json.dict(), commit=True)
    return Success(22)


@icon_api.route("/<icon_id>", methods=["PUT"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(23)),
    tags=["图标"],
)
def update_icon(icon_id, json: IconInSchema):
    """
    更新图标信息
    """
    icon = Icon.get(id=icon_id)
    if icon:
        icon.update(
            id=icon_id,
            progress="ok",
            **json.dict(),
            commit=True,
        )
        return Success(23)
    raise IconNotFound


@icon_api.route("/reopen/<icon_id>", methods=["POST", "PUT"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(23)),
    tags=["图标"],
)
def reopen_icon(icon_id):
    """
    重新打开图标绘制需求
    """
    icon = Icon.get(id=icon_id)
    if icon:
        if icon.progress == "ok":
            icon.update(progess="reopen")
            return Success(23)
        raise IconCannotReopen
    raise IconNotFound


@icon_api.route("/<icon_id>", methods=["DELETE"])
# @permission_meta(name="删除图标", module="图标")
# @group_required
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(IconNotFound, Success(24)),
    tags=["图标"],
)
def delete_icon(icon_id):
    """
    传入id删除对应图标
    """
    icon = Icon.get(id=icon_id)
    if icon:
        # 删除图标，软删除
        icon.delete(commit=True)
        return Success(24)
    raise IconNotFound
