#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午3:01
# @Author  : Rain
# @Desc    : 自定义服务项接口
# @File    : user_service_item_resource.py


from flask_restful import reqparse, Resource
from app import admin_manager, db
from app.models import Const, CustomServiceItem, CustomServiceItemSchema, ServiceStatus, ProjectPhase, Project, ServiceItemCategory
from app.utils.utils import safe_session, merge
from sqlalchemy import or_


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


class CustomServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, usiid):
        item = CustomServiceItem.query.get_or_404(usiid)
        schema = CustomServiceItemSchema()
        result = schema.dump(item).data

        return {'item': result}, Const.STATUS_OK

    def post(self, usiid):
        usi = CustomServiceItem.query.get_or_404(usiid)
        args = parser.parse_args()
        merge(usi, args)

        with safe_session(db):
            db.session.add(usi)

        return {Const.MESSAGE_KEY: '定制订单修改成功'}, Const.STATUS_OK


class CustomServiceItemListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        args = search_parser.parse_args()

        category_id = args.get('id')
        uid = args.get('category_id')
        status = args.get('status')
        project_name = args.get('project_name')
        title = args.get('title')
        description = args.get('description')
        starttime = args.get('starttime')
        endtime = args.get('endtime')

        conditions = []

        if isinstance(uid, int):
            conditions.append(CustomServiceItem.id == uid)

        if isinstance(category_id, int):
            conditions.append(CustomServiceItem.category_id == category_id)

        if status:
            if status in ServiceStatus.__members__.keys():
                conditions.append(CustomServiceItem.status == ServiceStatus[status])

        if project_name:
            projects = Project.query.filter(Project.name.contains(project_name)).all()

            if len(projects) > 0:

                pids = [p.id for p in projects]

                pps = ProjectPhase.query.filter(ProjectPhase.project_id.in_(pids)).all()

                conditions.append(CustomServiceItem.ppid.in_([pp.id for pp in pps]))

        if title:
            conditions.append(CustomServiceItem.title.contains(title))

        if description:
            conditions.append(CustomServiceItem.description.contains(description))

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= CustomServiceItem.timestamp <= int(endtime))

        items = CustomServiceItem.query.filter(or_(*conditions)).all()

        for item in items:
            item.category_name = ServiceItemCategory.query.get(item.category_id).name

        schema = CustomServiceItemSchema(many=True)
        result = schema.dump(items).data

        return {'items': result}, Const.STATUS_OK

    def post(self):
        item = CustomServiceItem()
        args = parser.parse_args()
        item.status = ServiceStatus.Submitted

        merge(item, args)

        with safe_session(db):
            db.session.add(item)

        return {Const.MESSAGE_KEY: '定制服务项创建成功'}, Const.STATUS_OK
