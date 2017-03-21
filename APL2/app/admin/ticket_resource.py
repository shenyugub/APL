#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:30
# @Author  : Rain
# @Desc    : 工单接口
# @File    : TicketResource.py

from flask_restful import reqparse, Resource
from app.models import Ticket, TicketSchema, Const
from app import admin_manager, db
from app.utils.utils import merge, safe_session


parser = reqparse.RequestParser()
parser.add_argument('author_id', type=int, location='json', store_missing=False)
parser.add_argument('title', type=str, location='json', store_missing=False)
parser.add_argument('content', type=str, location='json', store_missing=False)
parser.add_argument('url', type=str, location='json', store_missing=False)
parser.add_argument('contact_name', type=str, location='json', store_missing=False)
parser.add_argument('contact_phone', type=str, location='json', store_missing=False)
parser.add_argument('timestamp', type=str, location='json', store_missing=False)


class TicketResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, tid):
        ticket = Ticket.query.get_or_404(tid)

        schema = TicketSchema()
        result = schema.dump(ticket).data

        return {'ticket': result}, Const.STATUS_OK

    def post(self, tid):
        ticket = Ticket.query.get_or_404(tid)
        args = parser.parse_args()
        merge(ticket, args)

        with safe_session(db):
            db.session.add(ticket)

        return {Const.MESSAGE_KEY: '工单表修改成功'}, Const.STATUS_OK


class TicketListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        ticket = Ticket.query.all()

        schema = TicketSchema(many=True)
        result = schema.dump(ticket).data

        return {'comment': result}, Const.STATUS_OK

    def post(self):

        ticket = Ticket()
        args = parser.parse_args()
        merge(ticket, args)

        with safe_session(db):
            db.session.add(ticket)

        return {Const.MESSAGE_KEY: '工单表创建成功'}, Const.STATUS_OK
