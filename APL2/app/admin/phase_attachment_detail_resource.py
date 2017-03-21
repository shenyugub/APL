#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 下午2:10
# @Author  : Rain
# @Desc    : 用户交付物详情接口
# @File    : phase_attachment_detail_resource.py

from flask_restful import reqparse, Resource
from app.utils.utils import merge, safe_session
from app.models import Const, PhaseAttachmentDetail, PhaseAttachmentDetailSchema
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('url', type=str, location='args', store_missing=False)
parser.add_argument('comment', type=str, location='args', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=int, location='args', store_missing=False)


class PhaseAttachmentDetailResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, padid):
        pad = PhaseAttachmentDetail.query.get_or_404(padid)
        schema = PhaseAttachmentDetailSchema()
        result = schema.dump(pad).data

        return {'detail': result}, Const.STATUS_OK

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

        pads = PhaseAttachmentDetail.query.filter_by(paid=padid).all()
        schema = PhaseAttachmentDetailSchema(many=True)
        result = schema.dump(pads).data

        return {'details': result}, Const.STATUS_OK

    def post(self):
        pad = PhaseAttachmentDetail()
        args = parser.parse_args()
        merge(pad, args)

        with safe_session(db):
            db.session.add(pad)

        return {Const.MESSAGE_KEY: '新增附件信息成功'}, Const.STATUS_OK
