#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/6 下午5:10
# @Author  : Rain
# @Desc    : 管理员模块通用接口
# @File    : login_resource.py

from flask import session
from flask_restful import Resource, reqparse
from app import admin_manager, db
from app.models import Admin, Const, Permissions
from app.utils.utils import safe_session


class LoginResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='请输入用户名', location='json', store_missing=False)
        self.parser.add_argument('password', type=str, required=True, help='请输入密码', location='json', store_missing=False)
        self.parser.add_argument('vcode', type=str, required=True, help='请输入验证码', location='json', store_missing=False)
        super(LoginResource, self).__init__()

    def get(self):
        return {'hello': 'admin api v1'}, 200

    def post(self):
        args = self.parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        vcode = args.get('vcode', '')

        server_code = session.get('vcode', '')

        if vcode.upper() != server_code.upper():
            return {Const.MESSAGE_KEY: '验证码错误'}, Const.STATUS_ERROR

        user = Admin.query.filter_by(email=username).first()

        if not user:
            return {Const.MESSAGE_KEY: '该用户不存在'}, Const.STATUS_ERROR

        if not user.verify_password(password):
            return {Const.MESSAGE_KEY: '密码错误'}, Const.STATUS_ERROR

        admin_manager.login(user)
        session.pop('vcode')

        return {Const.MESSAGE_KEY: '登陆成功'}, Const.STATUS_OK


class ResetPasswordResource(Resource):

    def __init__(self):

        self.parseer = reqparse.RequestParser()
        self.parseer.add_argument('old_pwd', type=str, required=True, help='请输入原密码', location='json', store_missing=False)
        self.parseer.add_argument('new_pwd', type=str, required=True, help='请输入新密码', location='json', store_missing=False)
        super(ResetPasswordResource, self).__init__()

    @admin_manager.permissions_required(Permissions.ResetPassword.value)
    def post(self):

        args = self.parseer.parse_args()
        user = admin_manager.current_user

        if user.verify_password(args.get('old_pwd')):
            user.password = args.get('new_pwd')

            with safe_session(db):
                db.session.add(user)

            return {Const.MESSAGE_KEY: '密码修改成功'}, Const.STATUS_OK

        return {Const.MESSAGE_KEY: '原密码错误'}, Const.STATUS_ERROR
