#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/17 上午9:58
# @Author  : Rain
# @Desc    : OSS文件访问接口
# @File    : file_resource.py

from flask_restful import Resource
from app.models import File
from app import admin_manager
from app.utils.sts import get_file_url


class FileResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, name):
        file = File.query.filter_by(server_name=name).first()

        if file:
            url = get_file_url(file.server_name, file.local_name)
            return url

        return None
