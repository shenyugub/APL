#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午3:01
# @Author  : Rain
# @Desc    : 用户服务项管理
# @File    : user_service_item_resource.py

from flask_restful import reqparse, Resource
from app import admin_manager, db
from app.models import Const, UserServiceItem, UserServiceItemSchema, ServiceStatus, ServiceItem, ProjectPhase, PaginationSchema
from app.utils.utils import safe_session, merge
from sqlalchemy import and_
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('ppid', type=int, location='json', store_missing=False)
parser.add_argument('service_id', type=str, location='json', store_missing=False)
parser.add_argument('price', type=int, default=0, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=int, location='args', store_missing=False)
search_parser.add_argument('status', type=str, location='args', store_missing=False)
search_parser.add_argument('project_name', type=str, location='args', store_missing=False)
search_parser.add_argument('service_name', type=str, location='args', store_missing=False)
search_parser.add_argument('service_category_id', type=int, nullable=True, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class UserServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, usiid):
        item = UserServiceItem.query.get_or_404(usiid)
        schema = UserServiceItemSchema()
        result = schema.dump(item).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, usiid):
        usi = UserServiceItem.query.get_or_404(usiid)
        args = parser.parse_args()
        merge(usi, args, ignore=('ppid', 'service_id'))

        with safe_session(db):
            db.session.add(usi)

        return {Const.MESSAGE_KEY: '用户订单修改成功'}, Const.STATUS_OK


class UserServiceItemListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        args = search_parser.parse_args()

        uid = args.get('id')
        status = args.get('status')
        project_name = args.get('project_name')
        service_name = args.get('service_name')
        service_category_id = args.get('service_category_id')
        starttime = args.get('starttime')
        endtime = args.get('endtime')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        conditions = []

        if isinstance(uid, int):
            conditions.append(UserServiceItem.id == uid)

        if status in ServiceStatus.__members__.keys():
            conditions.append(UserServiceItem.status == ServiceStatus[status])

        if project_name:
            conditions.append(UserServiceItem.project_name.contains(project_name))

        if service_name:
            conditions.append(UserServiceItem.service_name.contains(service_name))

        if service_category_id:
            conditions.append(UserServiceItem.service_category_id == service_category_id)

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= UserServiceItem.timestamp <= int(endtime))

        pagination = UserServiceItem.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)
        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(UserServiceItemSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        args = parser.parse_args()
        service_id = args.get('service_id')
        ppid = args.get('ppid')

        item = UserServiceItem()
        si = ServiceItem.query.get(service_id)
        pp = ProjectPhase.query.get(ppid)
        if si and pp:
            item.project_name = pp.project_name
            item.phase_name = pp.phase_name
            item.service_name = si.name
            item.price = si.price
            item.status = ServiceStatus.Submitting
            merge(item, args)

            with safe_session(db):
                db.session.add(item)

            return {Const.MESSAGE_KEY: '服务项创建成功'}, Const.STATUS_OK
        return {Const.MESSAGE_KEY: '服务项创建失败'}, Const.STATUS_ERROR


class BillListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()

        usid = args.get('id')
        project_name = args.get('project_name')
        starttime = args.get('starttime')
        endtime = args.get('endtime')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        conditions = []

        if isinstance(usid, int):
            conditions.append(UserServiceItem.id == usid)

        if project_name:
            conditions.append(UserServiceItem.project_name.contains(project_name))

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= UserServiceItem.timestamp <= int(endtime))

        pagination = UserServiceItem.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)
        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(UserServiceItemSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK
