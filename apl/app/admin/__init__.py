#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/15 下午4:04
# @Author  : Rain
# @Desc    : 管理员模块入口文件
# @File    : __init__.py

from flask import Blueprint
from app import admin_manager
from app.models import Admin, Const


admin = Blueprint('admin', __name__)
from .api.v1 import api_v1


@admin_manager.user_loader
def user_loader(uid):
    if not isinstance(uid, (int, str)):
        return None

    return Admin.query.get(uid)


@admin_manager.failure_handler
def failure_handler():
    return {Const.MESSAGE_KEY: '您尚未登录或权限不足'}, Const.STATUS_DENIED


@admin_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, admin_manager.expires, admin_manager.salt)
