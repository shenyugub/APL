#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午3:01
# @Author  : Rain
# @Desc    : 用户服务项管理
# @File    : user_service_item_resource.py

from flask_restful import reqparse, Resource
from app import admin_manager, db
from app.models import Const, UserServiceItem, UserServiceItemSchema, ServiceStatus, ServiceItem, ProjectPhase, Project, ServiceItemCategory
from app.utils.utils import safe_session, merge
from sqlalchemy import or_, and_


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
search_parser.add_argument('service_category', type=str, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)


class UserServiceItemResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, usiid):
        item = UserServiceItem.query.get_or_404(usiid)
        _convert_id_to_name(item)
        schema = UserServiceItemSchema()
        result = schema.dump(item).data

        return {'item': result}, Const.STATUS_OK

    def post(self, usiid):
        usi = UserServiceItem.query.get_or_404(usiid)
        args = parser.parse_args()
        merge(usi, args)

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
        service_category = args.get('service_category')
        starttime = args.get('starttime')
        endtime = args.get('endtime')

        conditions = []

        if isinstance(uid, int):
            conditions.append(UserServiceItem.id == uid)

        if status:
            if status in ServiceStatus.__members__.keys():
                conditions.append(UserServiceItem.status == ServiceStatus[status])

        if project_name:
            projects = Project.query.filter(Project.name.contains(project_name)).all()

            if len(projects) > 0:

                pids = [p.id for p in projects]

                pps = ProjectPhase.query.filter(ProjectPhase.project_id.in_(pids)).all()

                conditions.append(UserServiceItem.ppid.in_([pp.id for pp in pps]))

        if service_name:
            services = ServiceItem.query.filter(ServiceItem.name.contains(service_name)).all()
            if len(services) > 0:
                sids = [s.id for s in services]
                conditions.append(UserServiceItem.service_id.in_(sids))

        if service_category:
            categorys = ServiceItemCategory.query.filter(ServiceItemCategory.name.contains(service_category)).all()
            if len(categorys) > 0:
                cids = [c.id for c in categorys]

                services = ServiceItem.query.filter(ServiceItem.category_id.in_(cids)).all()
                conditions.append(UserServiceItem.service_id.in_([s.id for s in services]))

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= UserServiceItem.timestamp <= int(endtime))

        items = UserServiceItem.query.filter(or_(*conditions)).all()

        for item in items:
            _convert_id_to_name(item)

        schema = UserServiceItemSchema(many=True)
        result = schema.dump(items).data

        return {'items': result}, Const.STATUS_OK

    def post(self):

        args = parser.parse_args()
        service_id = args.get('service_id')
        sids = service_id.split(',')
        if len(sids) > 0:
            sids = [int(sid) for sid in sids]

            for sid in sids:
                item = UserServiceItem()
                ss = ServiceItem.query.get(sid)
                if ss:
                    item.service_name = ss.name
                    item.price = ss.price
                    item.status = ServiceStatus.Submitted
                    merge(item, args)

                    with safe_session(db):
                        db.session.add(item)

        return {Const.MESSAGE_KEY: '服务项创建成功'}, Const.STATUS_OK


def _convert_id_to_name(item):
    service = ServiceItem.query.get(item.service_id)
    if service:
        item.service_name = service.name

    pp = ProjectPhase.query.get(item.ppid)

    if pp and pp.project:
        item.project_name = pp.project.name


class BillListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()

        uid = args.get('id')
        project_name = args.get('project_name')
        starttime = args.get('starttime')
        endtime = args.get('endtime')

        conditions = []

        if isinstance(uid, int):
            conditions.append(UserServiceItem.id == uid)

        if project_name:
            projects = Project.query.filter(Project.name.contains(project_name)).all()

            if len(projects) > 0:

                pids = [p.id for p in projects]

                pps = ProjectPhase.query.filter(ProjectPhase.project_id.in_(pids)).all()

                conditions.append(UserServiceItem.ppid.in_([pp.id for pp in pps]))

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= UserServiceItem.timestamp <= int(endtime))

        items = UserServiceItem.query.filter(or_(*conditions)).all()

        for item in items:
            _convert_id_to_name(item)

        schema = UserServiceItemSchema(many=True)
        result = schema.dump(items).data

        return {'bills': result}, Const.STATUS_OK
