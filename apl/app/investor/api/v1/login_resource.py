#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/6 下午5:10
# @Author  : Rain
# @Desc    : 管理员模块通用接口
# @File    : login_resource.py


from flask_restful import Resource, reqparse


class LoginResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json', store_missing=False)
        self.parser.add_argument('password', type=str, required=True, help='请输入密码', location='json', store_missing=False)
        self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json', store_missing=False)
        super(LoginResource, self).__init__()

    def get(self):
        return {'hello': 'investor api v1'}, 200
