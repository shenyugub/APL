#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午2:10
# @Author  : Rain
# @Desc    : 用户交付物详情接口
# @File    : phase_attachment_detail_resource.py

from flask_restful import reqparse, Resource
from app.utils.utils import merge, safe_session
from app.models import Const, PhaseAttachmentDetail, PhaseAttachmentDetailSchema, PaginationSchema
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('url', type=str, location='args', store_missing=False)
parser.add_argument('comment', type=str, location='args', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=int, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class PhaseAttachmentDetailResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, padid):
        pad = PhaseAttachmentDetail.query.get_or_404(padid)
        schema = PhaseAttachmentDetailSchema()
        result = schema.dump(pad).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, padid):

        pad = PhaseAttachmentDetail.query.get_or_404(padid)
        args = parser.parse_args()
        merge(pad, args)

        with safe_session(db):
            db.session.add(pad)

        return {Const.MESSAGE_KEY: '附件信息修改成功'}, Const.STATUS_OK


class PhaseAttachmentDetailListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        args = search_parser.parse_args()
        padid = args.get('id')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = PhaseAttachmentDetail.query.filter_by(paid=padid).paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(PhaseAttachmentDetailSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        pad = PhaseAttachmentDetail()
        args = parser.parse_args()
        merge(pad, args)

        with safe_session(db):
            db.session.add(pad)

        return {Const.MESSAGE_KEY: '新增附件信息成功'}, Const.STATUS_OK
