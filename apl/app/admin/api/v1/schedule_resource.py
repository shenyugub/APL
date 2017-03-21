#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:28
# @Author  : Rain
# @Desc    : 约谈接口
# @File    : schedule_resource.py

from flask_restful import Resource, reqparse
from app.models import Schedule, ScheduleSchema, Const, PaginationSchema
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('time', type=str, location='json', store_missing=False)
parser.add_argument('from_id', type=int, location='json', store_missing=False)
parser.add_argument('to_id', type=int, location='json', store_missing=False)
parser.add_argument('project_id', type=int, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class ScheduleResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, sid):
        schedul = Schedule.query.get_or_404(sid)
        schema = ScheduleSchema()
        result = schema.dump(schedul).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, sid):
        schedule = Schedule.query.get_or_404(sid)
        args = parser.parse_args()
        merge(schedule, args, ignore=('from_id', 'to_id', 'project_id'))

        with safe_session(db):
            db.session.add(schedule)
        return {Const.MESSAGE_KEY: '修改约谈表成功'}, Const.STATUS_OK


class ScheduleListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Schedule.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(ScheduleSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        schedule = Schedule()

        args = parser.parse_args()
        merge(schedule, args)

        with safe_session(db):
            db.session.add(schedule)

        return {Const.MESSAGE_KEY: '约谈记录成功'}, Const.STATUS_OK
