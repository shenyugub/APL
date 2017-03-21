#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/10 下午4:01
# @Author  : Rain
# @Desc    : 管理员接口
# @File    : admin_resource.py

from flask_restful import Resource, reqparse
from app.models import Admin, AdminSchema, Const, PaginationSchema
from app import admin_manager, db
from app.utils.utils import safe_session, merge
import sqlalchemy
from flask import current_app
from marshmallow import fields
from app.exceptions import EmailExistsException


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('email', type=str, location='json', store_missing=False)
parser.add_argument('password', type=str, location='json', store_missing=False)
parser.add_argument('dept_id', type=int, location='json', store_missing=False)
parser.add_argument('role_id', type=int, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class AdminResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, aid):

        admin = Admin.query.get_or_404(aid)
        schema = AdminSchema()
        result = schema.dump(admin).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, aid):

        admin = Admin.query.get_or_404(aid)
        args = parser.parse_args()
        # TODO，要判断权限来决定能否更改角色，否则自己改成超级管理员，就是漏洞了；不允许更改自己的角色
        merge(admin, args, ignore=('email',))  # 不允许修改邮箱

        with safe_session(db):
            db.session.add(admin)

        return {Const.MESSAGE_KEY: '管理员信息修改成功'}, Const.STATUS_OK


class AdminListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Admin.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(AdminSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        admin = Admin()
        args = parser.parse_args()
        merge(admin, args)

        try:
            with safe_session(db):
                db.session.add(admin)
        except sqlalchemy.exc.IntegrityError:
            raise EmailExistsException()

        return {Const.MESSAGE_KEY: '成功创建管理员'}, Const.STATUS_OK
