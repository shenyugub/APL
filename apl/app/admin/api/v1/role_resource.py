#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/6 下午5:11
# @Author  : Rain
# @Desc    : 角色接口
# @File    : role_resource.py

from flask_restful import Resource, reqparse
from app.models import Role, Const, RoleSchema, Permission, RolePermission, PaginationSchema
from app import admin_manager, db
from app.utils.utils import safe_session, merge
from flask import current_app
from marshmallow import fields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)
parser.add_argument('permissions', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class RoleResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, rid):

        role = Role.query.get_or_404(rid)
        schema = RoleSchema()
        result = schema.dump(role).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, rid):

        role = Role.query.get_or_404(rid)
        args = parser.parse_args()
        merge(role, args, ignore=('permissions',))

        with safe_session(db):
            db.session.add(role)

        return {Const.MESSAGE_KEY: '角色修改成功'}, Const.STATUS_OK


class RoleListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Role.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(RoleSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        role = Role()
        args = parser.parse_args()
        ps = args.get('permissions')

        if ps:
            ps = ps.split(',')

            for p in ps:
                permission = Permission.query.get(int(p))

                if permission:
                    db.session.expunge(permission)
                    rp = RolePermission()
                    rp.permission = permission
                    role.permissions.append(rp)

            with safe_session(db):
                db.session.add(role)

        merge(role, args, ignore=('permissions',))

        with safe_session(db):
            db.session.add(role)

        return {Const.MESSAGE_KEY: '角色创建成功'}, Const.STATUS_OK

