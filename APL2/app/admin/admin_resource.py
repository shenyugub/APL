#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/10 下午4:01
# @Author  : Rain
# @Desc    : 管理员接口
# @File    : admin_resource.py

from flask_restful import Resource, reqparse
from app.models import Admin, AdminSchema, Const
from app import admin_manager, db
from app.utils.utils import safe_session, merge
import sqlalchemy


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('email', type=str, location='json', store_missing=False)
parser.add_argument('password', type=str, location='json', store_missing=False)
parser.add_argument('dept_id', type=int, location='json', store_missing=False)
parser.add_argument('role_id', type=int, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)


class AdminResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, aid):

        admin = Admin.query.get_or_404(aid)
        admin.dept_name = admin.department.name
        admin.role_name = admin.role.name
        schema = AdminSchema()
        result = schema.dump(admin).data

        return {'admin': result}, Const.STATUS_OK

    def post(self, aid):

        admin = Admin.query.get_or_404(aid)

        args = parser.parse_args()

        merge(admin, args, ignore=('email',))  # 不允许修改邮箱

        with safe_session(db):
            db.session.add(admin)

        return {Const.MESSAGE_KEY: '管理员信息修改成功'}, Const.STATUS_OK


class AdminListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        admins = Admin.query.all()

        for a in admins:
            a.dept_name = a.department.name
            a.role_name = a.role.name

        schema = AdminSchema(many=True)
        result = schema.dump(admins).data

        return {'admins': result}, Const.STATUS_OK

    def post(self):

        admin = Admin()
        args = parser.parse_args()
        merge(admin, args)

        try:
            with safe_session(db):
                db.session.add(admin)
        except sqlalchemy.exc.IntegrityError as e:
            print('create admin error:', e)
            return {Const.MESSAGE_KEY: '创建管理员失败，该邮箱地址已存在'}, Const.STATUS_ERROR

        return {Const.MESSAGE_KEY: '成功创建管理员'}, Const.STATUS_OK
