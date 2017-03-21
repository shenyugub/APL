#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午3:01
# @Author  : Rain
# @Desc    : 自定义服务项接口
# @File    : user_service_item_resource.py


from flask_restful import reqparse, Resource
from app import admin_manager, db
from app.models import Const, CustomServiceItem, CustomServiceItemSchema, ServiceStatus, PaginationSchema
from app.utils.utils import safe_session, merge
from sqlalchemy import and_
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('ppid', type=str, location='json', store_missing=False)
parser.add_argument('category_id', type=str, location='json', store_missing=False)
parser.add_argument('title', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('price', type=str, default=0, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=int, location='args', store_missing=False)
search_parser.add_argument('category_id', type=int, location='args', store_missing=False)
search_parser.add_argument('status', type=str, location='args', store_missing=False)
search_parser.add_argument('project_name', type=str, location='args', store_missing=False)
search_parser.add_argument('title', type=str, location='args', store_missing=False)
search_parser.add_argument('description', type=str, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class CustomServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, usiid):
        item = CustomServiceItem.query.get_or_404(usiid)
        schema = CustomServiceItemSchema()
        result = schema.dump(item).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, usiid):
        item = CustomServiceItem.query.get_or_404(usiid)
        args = parser.parse_args()
        merge(item, args, ignore=('ppid', 'category_id'))

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '定制订单修改成功'}, Const.STATUS_OK


class CustomServiceItemListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        args = search_parser.parse_args()

        csid = args.get('id')
        category_id = args.get('category_id')
        status = args.get('status')
        project_name = args.get('project_name')
        title = args.get('title')
        description = args.get('description')
        starttime = args.get('starttime')
        endtime = args.get('endtime')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        conditions = []

        # 通过 ID 查询
        if isinstance(csid, int):
            conditions.append(CustomServiceItem.id == csid)

        # 通过类别查询
        if isinstance(category_id, int):
            conditions.append(CustomServiceItem.category_id == category_id)

        # 通过状态查询
        if status in ServiceStatus.__members__.keys():
            conditions.append(CustomServiceItem.status == ServiceStatus[status])

        # 通过项目名查询
        if project_name:
            conditions.append(CustomServiceItem.project_name.contains(project_name))

        # 通过标题查询
        if title:
            conditions.append(CustomServiceItem.title.contains(title))

        # 通过描述查询
        if description:
            conditions.append(CustomServiceItem.description.contains(description))

        # 通过创建时间查询
        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= CustomServiceItem.timestamp <= int(endtime))

        pagination = CustomServiceItem.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(CustomServiceItemSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        item = CustomServiceItem()
        args = parser.parse_args()

        merge(item, args)
        item.status = ServiceStatus.Submitting

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '定制服务项创建成功'}, Const.STATUS_OK
