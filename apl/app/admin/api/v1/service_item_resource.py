#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午2:26
# @Author  : Rain
# @Desc    : 系统服务项接口
# @File    : service_item_resource.py

from flask_restful import Resource, reqparse
from app.models import ServiceItem, ServiceItemSchema, Const, PaginationSchema
from app.utils.utils import merge, safe_session
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('category_id', type=int, location='json', store_missing=False)
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('desc', type=str, location='json', store_missing=False)
parser.add_argument('price', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class ServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, sid):
        item = ServiceItem.query.get_or_404(sid)
        item.category_name = item.category.name
        schema = ServiceItemSchema()
        result = schema.dump(item).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, sid):
        item = ServiceItem.query.get_or_404(sid)
        args = parser.parse_args()
        merge(item, args, ignore=('category_id',))

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '服务项修改成功'}, Const.STATUS_OK


class ServiceItemListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = ServiceItem.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(ServiceItemSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        item = ServiceItem()
        args = parser.parse_args()
        merge(item, args)

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '服务项添加成功'}, Const.STATUS_OK
