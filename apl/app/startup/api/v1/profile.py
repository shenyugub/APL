# -*- coding: utf-8 -*-
from app.models import StartupSchema, PaginationSchema, Const
from flask import current_app
from flask_restful import Resource
from sqlalchemy import and_
from marshmallow import fields

from app.utils.utils import merge, safe_session
from app import user_manager, db

from .parsers import profile_parser, password_reset_parser


class ProfileHandler(Resource):

    # method_decorators = [user_manager.login_required()]

    def get(self):
        user = user_manager.current_user
        schema = StartupSchema()
        result = schema.dump(user).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def put(self):
        user = user_manager.current_user
        args = profile_parser.parse_args()
        try:
            merge(user, args)
            with safe_session(db):
                db.session.add(user)
        except Exception as e:
            print(e)
            return {Const.MESSAGE_KEY: '接口请求失败'}, Const.STATUS_ERROR
        return {Const.MESSAGE_KEY: '资料修改成功'}, Const.STATUS_OK

    def post(self):
        raise Exception("Post method is not allow")

    def post(self):
        raise Exception("Delete method is not allow")


class PasswordHandler(Resource):

    def put(self):
        user = user_manager.current_user
        args = password_reset_parser.parse_args()
        if user.verify_password(args.get('old_pwd')):
            try:
                user.password = args.get('new_pwd')
                with safe_session(db):
                    db.session.add(user)
                return {Const.MESSAGE_KEY: '密码修改成功'}, Const.STATUS_OK
            except Exception as e:
                print(e)
                return {Const.MESSAGE_KEY: '接口请求失败'}, Const.STATUS_ERROR
        return {Const.MESSAGE_KEY: '原密码错误'}, Const.STATUS_ERROR
