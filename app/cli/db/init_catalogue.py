"""
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from typing import List

from lin.db import db

from app.model.icon_manager.catalogue_model import Catalogue

names: List[str] = [
    '交通位置',
    '休闲娱乐',
    '商业办公',
    '学习教育',
    '影音图像',
    '游戏',
    '生活服务',
    '系统工具',
    '网上购物',
    '资讯阅读',
    '运动健康',
    '通讯社交',
    '金融理财'
]
name_ens: List[str] = [
    'Traffic and Location',
    'Leisure and Entertainment',
    'Commercial Office',
    'Learning and Education',
    'Audiovisual Image',
    'Game',
    'Domestic Services',
    'System Tools',
    'Online Shopping',
    'Information Reading',
    'Sports Health',
    'Communication and Social',
    'Financial Management',

]


def init_catalogue():
    with db.auto_commit():
        # 添加
        for index in range(0, 13):
            catalogue: Catalogue = Catalogue()
            catalogue.id = index + 1
            catalogue.name = names[index]
            catalogue.name_en = name_ens[index]
            db.session.add(catalogue)
