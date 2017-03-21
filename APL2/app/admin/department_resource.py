#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午4:14
# @Author  : Rain
# @Desc    : 部门接口
# @File    : department_resource.py


from flask_restful import Resource, reqparse
from app.models import Department, DepartmentSchema, Const
from app.utils.utils import safe_session, merge
from app import admin_manager, db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)


class DepartmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, did):
        department = Department.query.get_or_404(did)
        schema = DepartmentSchema()
        result = schema.dump(department).data

        return {'department': result}, Const.STATUS_OK

    def post(self, did):
        department = Department.query.get_or_404(did)
        args = parser.parse_args()
        merge(department, args)

        with safe_session(db):
            db.session.add(department)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class DepartmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        department = Department.query.all()
        schema = DepartmentSchema(many=True)
        result = schema.dump(department).data

        return {'departments': result}, Const.STATUS_OK

    def post(self):
        department = Department()
        args = parser.parse_args()
        merge(department, args)

        with safe_session(db):
            db.session.add(department)

        return {Const.MESSAGE_KEY: '部门创建成功'}, Const.STATUS_OK
