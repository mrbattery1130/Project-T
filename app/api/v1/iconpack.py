from flask import request
from lin.apidoc import api, DocResponse
from lin.exception import Success
from lin.jwt import login_required
from lin.redprint import Redprint

from app.exception.api import IconpackNotFound
from app.model.icon_manager.iconpack_model import Iconpack
from app.validator.schema import IconpackOutSchema, IconpackSchemaList, AuthorizationSchema, IconpackInSchema

iconpack_api = Redprint('iconpack')


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
    headers=AuthorizationSchema,
    json=IconpackInSchema,
    resp=DocResponse(Success(16)),
    tags=["图标包"],
)
def create_iconpack():
    """
    创建图标包
    """
    iconpack_schema = request.context.json
    Iconpack.create(**iconpack_schema.dict(), commit=True)
    return Success(16)


@iconpack_api.route("/<iconpack_id>", methods=["PUT"])
@login_required
@api.validate(
    headers=AuthorizationSchema,
    json=IconpackInSchema,
    resp=DocResponse(Success(17)),
    tags=["图标包"],
)
def update_iconpack(iconpack_id):
    """
    更新图标包信息
    """
    iconpack_schema = request.context.json
    iconpack = Iconpack.get(id=iconpack_id)
    if iconpack:
        iconpack.update(
            id=iconpack_id,
            **iconpack_schema.dict(),
            commit=True,
        )
        return Success(17)
    raise IconpackNotFound


@iconpack_api.route("/<iconpack_id>", methods=["DELETE"])
# @permission_meta(name="删除图标包", module="图标")
# @group_required
@login_required
@api.validate(
    headers=AuthorizationSchema,
    resp=DocResponse(IconpackNotFound, Success(18)),
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
        return Success(18)
    raise IconpackNotFound
