#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午4:14
# @Author  : Rain
# @Desc    : 部门接口
# @File    : department_resource.py


from flask_restful import Resource, reqparse
from app.models import Department, DepartmentSchema, Const, PaginationSchema
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from flask import current_app
from marshmallow import fields

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('status', type=bool, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class DepartmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, did):
        department = Department.query.get_or_404(did)
        schema = DepartmentSchema()
        result = schema.dump(department).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

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
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Department.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(DepartmentSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        department = Department()
        args = parser.parse_args()
        merge(department, args)

        with safe_session(db):
            db.session.add(department)

        return {Const.MESSAGE_KEY: '部门创建成功'}, Const.STATUS_OK
