#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:26
# @Author  : Rain
# @Desc    : 权限接口
# @File    : permission_resource.py

from flask_restful import reqparse, Resource
from app.models import Permission, PermissionSchema, Const, PaginationSchema
from app.utils.utils import merge, safe_session
from app import admin_manager, db
import sqlalchemy
from flask import current_app
from marshmallow import fields
from app.exceptions import IllegalPermissionValueException


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class PermissionResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, pid):
        permission = Permission.query.get_or_404(pid)
        schema = PermissionSchema()
        result = schema.dump(permission).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, pid):
        permission = Permission.query.get_or_404(pid)
        args = parser.parse_args()
        merge(permission, args)

        with safe_session(db):
            db.session.add(permission)

        return {Const.MESSAGE_KEY: '权限修改成功'}, Const.STATUS_OK


class PermissionListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Permission.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(PermissionSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        args = parser.parse_args()

        permission = Permission()
        merge(permission, args)

        try:
            with safe_session(db):
                db.session.add(permission)
        except sqlalchemy.exc.IntegrityError:
            raise IllegalPermissionValueException()

        return {Const.MESSAGE_KEY: '权限创建成功'}, Const.STATUS_OK
