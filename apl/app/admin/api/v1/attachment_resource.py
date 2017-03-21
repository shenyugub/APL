#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午21:24
# @Author  : Rain
# @Desc    : 系统交付物接口
# @File    : attachment_resource.py


from flask_restful import reqparse, Resource
from app.models import Attachment, AttachmentSchema, Const, PaginationSchema
from app.utils.utils import merge, safe_session
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('url', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class AttachmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, aid):

        attachment = Attachment.query.get_or_404(aid)
        schema = AttachmentSchema()
        result = schema.dump(attachment).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, aid):
        attachment = Attachment.query.get_or_404(aid)
        args = parser.parse_args()
        merge(attachment, args)

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '修改交付物表成功'}, Const.STATUS_OK


class AttachmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Attachment.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(AttachmentSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        attachment = Attachment()
        args = parser.parse_args()

        merge(attachment, args)

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '交付物创建成功'}
