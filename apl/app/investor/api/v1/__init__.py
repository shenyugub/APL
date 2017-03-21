#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/21 上午12:45
# @Author  : Rain
# @Desc    :
# @File    : __init__.py.py

from .login_resource import LoginResource
from flask_restful import Api
from app.exceptions import errors
from app.investor import investor


api_v1 = Api(investor, prefix='/api/v1', catch_all_404s=True, errors=errors)
api_v1.add_resource(LoginResource, '/')
