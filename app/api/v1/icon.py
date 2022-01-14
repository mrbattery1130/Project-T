from lin.apidoc import api, DocResponse
from lin.redprint import Redprint

from app.exception.api import IconNotFound
from app.model.icon_manager.icon_model import Icon
from app.validator.schema import IconOutSchema

icon_api = Redprint('icon')


@icon_api.route('/<icon_id>')
@api.validate(
    resp=DocResponse(IconNotFound, r=IconOutSchema),
    tags=['App'],
)
def get_icon(icon_id: int):
    """
    获取id指定分类的信息
    """
    icon: Icon = Icon.get(id=icon_id)
    if icon:
        return icon
    raise IconNotFound
