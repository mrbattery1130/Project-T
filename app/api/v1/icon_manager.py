from typing import List

from flask.json import jsonify
from lin.redprint import Redprint

from app.model.icon_manager.app_model import App

icon_manager_api = Redprint('icon_manager')


@icon_manager_api.route('/app', methods=['GET'])
def get_apps():
    apps: List[App] = App.get_all_apps()
    return jsonify(apps)


@icon_manager_api.route('/app', methods=['POST'])
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
