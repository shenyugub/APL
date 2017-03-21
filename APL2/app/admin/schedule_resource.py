#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:28
# @Author  : Rain
# @Desc    : 约谈接口
# @File    : schedule_resource.py

from flask_restful import Resource, reqparse
from app.models import Schedule, ScheduleSchema, Const
from app.utils.utils import safe_session, merge
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('time', type=str, location='json', store_missing=False)
parser.add_argument('from_id', type=int, location='json', store_missing=False)
parser.add_argument('to_id', type=int, location='json', store_missing=False)
parser.add_argument('project_id', type=int, location='json', store_missing=False)


class ScheduleResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, sid):
        schedul = Schedule.query.get_or_404(sid)
        schema = ScheduleSchema()
        result = schema.dump(schedul).data
        return {'schedule': result}, Const.STATUS_OK

    def post(self, sid):
        schedule = Schedule.query.get_or_404(sid)
        args = parser.parse_args()
        merge(schedule, args)

        with safe_session(db):
            db.session.add(schedule)
        return {Const.MESSAGE_KEY: '修改约谈表成功'}, Const.STATUS_OK


class ScheduleListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        schedule = Schedule.query.all()
        schema = ScheduleSchema(many=True)
        result = schema.dump(schedule).data
        return {'schedules': result}, Const.STATUS_OK

    def post(self):
        schedule = Schedule()

        args = parser.parse_args()
        merge(schedule, args)

        with safe_session(db):
            db.session.add(schedule)

        return {Const.MESSAGE_KEY: '约谈记录成功'}, Const.STATUS_OK
