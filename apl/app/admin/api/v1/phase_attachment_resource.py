#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午3:33
# @Author  : Rain
# @Desc    : 用户交付物接口
# @File    : PhaseAttachmentResource.py

from flask_restful import Resource, reqparse
from app.models import Const, PhaseAttachment, PhaseAttachmentSchema, AttachmentStatus, PaginationSchema
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from sqlalchemy import and_
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('phase_id', type=int, location='json', store_missing=False)
parser.add_argument('attachment_id', type=int, location='json', store_missing=False)
parser.add_argument('file_url', type=str, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)
parser.add_argument('comment', type=str, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('phase_name', type=str, location='args', store_missing=False)
search_parser.add_argument('attachment_name', type=str, location='args', store_missing=False)
search_parser.add_argument('status', type=str, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class PhaseAttachmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, paid):
        pa = PhaseAttachment.query.get_or_404(paid)
        schema = PhaseAttachmentSchema()
        result = schema.dump(pa).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, paid):
        pa = PhaseAttachment.query.get_or_404(paid)
        args = parser.parse_args()
        merge(pa, args, ignore=('phase_id', 'attachment_id'))

        with safe_session(db):
            db.session.add(pa)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class PhaseAttachmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        conditions = []
        args = search_parser.parse_args()
        phase_name = args.get('phase_name')
        attachment_name = args.get('attachment_name')
        status = args.get('status')
        starttime = args.get('starttime')
        endtime = args.get('endtime')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        if phase_name:
            conditions.append(PhaseAttachment.phase_name.contains(phase_name))

        if attachment_name:
            conditions.append(PhaseAttachment.attachment_name.contains(attachment_name))

        if status in AttachmentStatus.__members__.values():
            conditions.append(PhaseAttachment.status == status)

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= PhaseAttachment.timestamp <= int(endtime))

        pagination = PhaseAttachment.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(PhaseAttachmentSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        pa = PhaseAttachment()
        args = parser.parse_args()
        merge(pa, args)

        with safe_session(db):
            db.session.add(pa)

        return {Const.MESSAGE_KEY: '创建成功'}, Const.STATUS_OK
