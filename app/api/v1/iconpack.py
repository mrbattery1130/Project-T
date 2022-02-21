from flask import Blueprint
from lin.apidoc import DocResponse
from lin.exception import Success
from lin.jwt import login_required

from app.api import api, AuthorizationBearerSecurity
from app.api.v1.exception import IconpackNotFound
from app.api.v1.model.iconpack_model import Iconpack
from app.api.v1.schema import IconpackOutSchema, IconpackSchemaList, IconpackInSchema

iconpack_api = Blueprint('iconpack', __name__)


@iconpack_api.route('/<iconpack_id>')
@api.validate(
    resp=DocResponse(IconpackNotFound, r=IconpackOutSchema),
    tags=["图标包"],
)
def get_iconpack(iconpack_id):
    """
    获取id指定图标包的信息
    """
    iconpack: Iconpack = Iconpack.get(id=iconpack_id)
    if iconpack:
        return iconpack
    raise IconpackNotFound


@iconpack_api.route('')
@api.validate(
    resp=DocResponse(r=IconpackSchemaList),
    tags=["图标包"],
)
def get_iconpacks():
    """
    获取图标包列表
    """
    return Iconpack.get(one=False)


@iconpack_api.route("", methods=["POST"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(25)),
    tags=["图标包"],
)
def create_iconpack(json: IconpackInSchema):
    """
    创建图标包
    """
    Iconpack.create(**json.dict(), commit=True)
    return Success(25)


@iconpack_api.route("/<iconpack_id>", methods=["PUT"])
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(Success(26)),
    tags=["图标包"],
)
def update_iconpack(iconpack_id, json: IconpackInSchema):
    """
    更新图标包信息
    """
    iconpack = Iconpack.get(id=iconpack_id)
    if iconpack:
        iconpack.update(
            id=iconpack_id,
            **json.dict(),
            commit=True,
        )
        return Success(26)
    raise IconpackNotFound


@iconpack_api.route("/<iconpack_id>", methods=["DELETE"])
# @permission_meta(name="删除图标包", module="图标")
# @group_required
@login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(IconpackNotFound, Success(27)),
    tags=["图标包"],
)
def delete_iconpack(iconpack_id):
    """
    传入id删除对应图标包
    """
    iconpack = Iconpack.get(id=iconpack_id)
    if iconpack:
        # 删除图标包，软删除
        iconpack.delete(commit=True)
        return Success(27)
    raise IconpackNotFound
