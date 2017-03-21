#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:26
# @Author  : Rain
# @Desc    : 权限接口
# @File    : permission_resource.py

from flask_restful import reqparse, Resource
from app.models import Permission, PermissionSchema, Const
from app.utils.utils import merge, safe_session
from app import admin_manager, db
import sqlalchemy

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)


class PermissionResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, pid):
        permission = Permission.query.get_or_404(pid)
        schema = PermissionSchema()
        result = schema.dump(permission).data

        return {'permission': result}, Const.STATUS_OK

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
        permission = Permission.query.all()
        schema = PermissionSchema(many=True)
        result = schema.dump(permission).data

        return {'permissions': result}, Const.STATUS_OK

    def post(self):
        args = parser.parse_args()

        # TODO 判断权限值是否是2N次方

        permission = Permission()
        merge(permission, args)

        try:
            with safe_session(db):
                db.session.add(permission)
        except sqlalchemy.exc.IntegrityError as e:
            print('create permission error:', e)
            return {Const.MESSAGE_KEY: '权限创建失败，权限值不能重复'}, Const.STATUS_ERROR

        return {Const.MESSAGE_KEY: '权限创建成功'}, Const.STATUS_OK
