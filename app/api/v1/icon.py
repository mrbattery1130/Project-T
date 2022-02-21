from flask import Blueprint
from lin.apidoc import DocResponse
from lin.exception import Success
from lin.jwt import login_required

from app.api import api, AuthorizationBearerSecurity
from app.api.v1.exception import IconNotFound
from app.api.v1.model.icon_model import Icon
from app.api.v1.schema import IconOutSchema, IconInSchema, IconSchemaList

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
    resp=DocResponse(r=IconSchemaList),
    tags=["图标"],
)
def get_icons():
    """
    获取图标列表，分页展示
    """
    return Icon.get(one=False)


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
            **json.dict(),
            commit=True,
        )
        return Success(23)
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
