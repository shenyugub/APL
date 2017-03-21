#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午2:26
# @Author  : Rain
# @Desc    : 系统服务项接口
# @File    : service_item_resource.py

from flask_restful import Resource, reqparse
from app.models import ServiceItem, ServiceItemSchema, Const
from app.utils.utils import merge, safe_session
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('category_id', type=int, location='json', store_missing=False)
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('desc', type=str, location='json', store_missing=False)
parser.add_argument('price', type=str, location='json', store_missing=False)


class ServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, sid):
        item = ServiceItem.query.get_or_404(sid)
        item.category_name = item.category.name
        schema = ServiceItemSchema()
        result = schema.dump(item).data

        return {'service_item': result}, Const.STATUS_OK

    def post(self, sid):
        item = ServiceItem.query.get_or_404(sid)
        args = parser.parse_args()
        merge(item, args)

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '服务项修改成功'}, Const.STATUS_OK


class ServiceItemListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        items = ServiceItem.query.all()

        for item in items:
            item.category_name = item.category.name

        schema = ServiceItemSchema(many=True)
        result = schema.dump(items).data

        return {'service_item_list': result}, Const.STATUS_OK

    def post(self):

        item = ServiceItem()
        args = parser.parse_args()
        merge(item, args)

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '服务项添加成功'}, Const.STATUS_OK
