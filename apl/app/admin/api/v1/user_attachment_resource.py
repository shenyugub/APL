#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午4:14
# @Author  : Rain
# @Desc    : 用户交付物接口
# @File    : comment_resource.py

from flask_restful import reqparse, Resource
from app.models import UserAttachment, UserAttachmentSchema, Const, PaginationSchema
from app.utils.utils import merge, safe_session
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('ppid', type=int, location='json', store_missing=False)
parser.add_argument('attachment_id', type=int, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)
parser.add_argument('url', type=str, location='json', store_missing=False)
parser.add_argument('comment', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class UserAttachmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, uaid):
        attachment = UserAttachment.query.get_or_404(uaid)
        schema = UserAttachmentSchema()
        result = schema.dump(attachment).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, uaid):
        attachment = UserAttachment.query.get_or_404(uaid)
        args = parser.parse_args()
        merge(attachment, args, ignore=('ppid', 'attachment_id'))

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '交付物修改成功'}, Const.STATUS_OK


class UserAttachmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = UserAttachment.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(UserAttachmentSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        attachment = UserAttachment()
        args = parser.parse_args()
        merge(attachment, args)

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '交付物发布成功'}, Const.STATUS_OK
