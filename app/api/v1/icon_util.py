# from flask import jsonify, g, Blueprint
# from lin.apidoc import DocResponse
#
# from app.api import api
# from app.api.v1.model.icon_spider import AppIconSpider
# from app.api.v1.schema import AppIconQuerySearchSchema, IconSpiderOutListSchema, \
#     PackageNameQuerySearchSchema, PackageNameSpiderOutListSchema
#
# icon_util_api = Blueprint('icon_util', __name__)
#
#
# @icon_util_api.route('/search', methods=['GET'])
# @api.validate(
#     query=AppIconQuerySearchSchema,
#     resp=DocResponse(r=IconSpiderOutListSchema),
#     tags=['图标工具'],
# )
# def search():
#     app_icons = AppIconSpider.search_by_package_name(g.package_name)
#     return {"app_icons": app_icons, "package_name": g.package_name}
#
#
# @icon_util_api.route('/search_package_name', methods=['GET'])
# @api.validate(
#     query=PackageNameQuerySearchSchema,
#     resp=DocResponse(r=PackageNameSpiderOutListSchema),
#     tags=['图标工具'],
# )
# def search_package_name():
#     package_names = AppIconSpider.search_package_name(g.app_name)
#     return jsonify(package_names)
