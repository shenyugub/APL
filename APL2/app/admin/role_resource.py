#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/6 下午5:11
# @Author  : Rain
# @Desc    : 角色接口
# @File    : role_resource.py

from flask_restful import Resource, reqparse
from app.models import Role, Const, RoleSchema, Permission, RolePermission
from app import admin_manager, db
from app.utils.utils import safe_session, merge


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)
parser.add_argument('permissions', type=str, location='json', store_missing=False)


class RoleResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, rid):

        role = Role.query.get_or_404(rid)
        schema = RoleSchema()
        result = schema.dump(role).data

        return {'role': result}, Const.STATUS_OK

    def post(self, rid):

        role = Role.query.get_or_404(rid)
        args = parser.parse_args()
        merge(role, args)

        with safe_session(db):
            db.session.add(role)

        return {Const.MESSAGE_KEY: '角色修改成功'}, Const.STATUS_OK


class RoleListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        roles = Role.query.all()
        schema = RoleSchema(many=True)
        result = schema.dump(roles).data

        return {'roles': result}, Const.STATUS_OK

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

