from flask import Blueprint
from lin import db
from lin.apidoc import DocResponse
from lin.exception import Success
from lin.jwt import login_required

from app.api import api, AuthorizationBearerSecurity
from app.api.v1.exception import IconpackNotFound, IconNotFound
from app.api.v1.model.app_model import App
from app.api.v1.model.icon_model import Icon
from app.api.v1.model.iconpack_model import Iconpack
from app.api.v1.schema import IconpackOutSchema, IconpackSchemaList, IconpackInSchema, \
    IconSchemaList, IconReqSchemaList

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


@iconpack_api.route("/req_list/<iconpack_id>", methods=["GET"])
# @login_required
@api.validate(
    security=[AuthorizationBearerSecurity],
    resp=DocResponse(r=IconReqSchemaList),
    tags=["图标包"],
)
def get_req_list(iconpack_id):
    """
    导出图标包需求列表
    """
    iconpack = Iconpack.get(id=iconpack_id)
    if iconpack:
        tup_list = db.session.query(
            Icon.id, App.id, App.name, App.name_en, Icon.progress
        ).join(App, Icon.app_id == App.id).filter(
            App.is_deleted == False,
            Icon.iconpack_id == iconpack_id,
            Icon.progress == "nok"
        ).all()
        if tup_list:
            print(tup_list)
            ret = []
            for tup in tup_list:
                ret.append(
                    {
                        "iconpack_id":iconpack_id,
                        "icon_id": tup[0],
                        "app_id": tup[1],
                        "app_name": tup[2],
                        "app_name_en": tup[3],
                        "progress": tup[4],
                    }
                )
            return ret
        raise IconNotFound
    raise IconpackNotFound
