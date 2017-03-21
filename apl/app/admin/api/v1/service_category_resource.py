#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午1:38
# @Author  : Rain
# @Desc    : 服务项类别接口
# @File    : service_category_resource.py

from app.models import ServiceItemCategory, ServiceItemCategorySchema, Const, PaginationSchema
from flask_restful import Resource, reqparse
from app.utils.utils import merge, safe_session
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class ServiceCategoryResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, sid):
        sc = ServiceItemCategory.query.get_or_404(sid)

        schema = ServiceItemCategorySchema()
        result = schema.dump(sc).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, sid):

        sc = ServiceItemCategory.query.get_or_404(sid)
        args = parser.parse_args()
        merge(sc, args)

        with safe_session(db):
            db.session.add(sc)

        return {Const.MESSAGE_KEY: '服务包类别修改成功'}, Const.STATUS_OK


class ServiceCategoryListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = ServiceItemCategory.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(ServiceItemCategorySchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        sc = ServiceItemCategory()
        args = parser.parse_args()
        merge(sc, args)

        with safe_session(db):
            db.session.add(sc)

        return {Const.MESSAGE_KEY: '服务包类别创建成功'}, Const.STATUS_OK
