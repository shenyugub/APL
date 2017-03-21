#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:30
# @Author  : Rain
# @Desc    : 工单接口
# @File    : TicketResource.py

from flask_restful import reqparse, Resource
from app.models import Ticket, TicketSchema, Const, PaginationSchema
from app import admin_manager, db
from app.utils.utils import merge, safe_session
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('author_id', type=int, location='json', store_missing=False)
parser.add_argument('title', type=str, location='json', store_missing=False)
parser.add_argument('content', type=str, location='json', store_missing=False)
parser.add_argument('url', type=str, location='json', store_missing=False)
parser.add_argument('contact_name', type=str, location='json', store_missing=False)
parser.add_argument('contact_phone', type=str, location='json', store_missing=False)
parser.add_argument('timestamp', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class TicketResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, tid):
        ticket = Ticket.query.get_or_404(tid)

        schema = TicketSchema()
        result = schema.dump(ticket).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, tid):
        ticket = Ticket.query.get_or_404(tid)
        args = parser.parse_args()
        merge(ticket, args, ignore=('author_id',))

        with safe_session(db):
            db.session.add(ticket)

        return {Const.MESSAGE_KEY: '工单表修改成功'}, Const.STATUS_OK


class TicketListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Ticket.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(TicketSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        ticket = Ticket()
        args = parser.parse_args()
        merge(ticket, args)

        with safe_session(db):
            db.session.add(ticket)

        return {Const.MESSAGE_KEY: '工单表创建成功'}, Const.STATUS_OK
