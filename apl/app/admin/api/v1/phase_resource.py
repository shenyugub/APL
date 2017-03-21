#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午5:08
# @Author  : Rain
# @Desc    : 系统项目阶段接口
# @File    : phase_resource.py


from flask_restful import Resource, reqparse
from app.models import Phase, PhaseSchema, Const, Attachment, PhaseAttachment, PaginationSchema
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('attachments', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class PhaseResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, pid):
        phase = Phase.query.get_or_404(pid)
        phase.atts = []
        for a in phase.attachments:
            phase.atts.append(a.attachment)

        schema = PhaseSchema(exclude=('atts.phase_id',))
        result = schema.dump(phase).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, pid):

        phase = Phase.query.get_or_404(pid)
        args = parser.parse_args()
        merge(phase, args, ignore=('attachments',))

        with safe_session(db):
            db.session.add(phase)

        return {Const.MESSAGE_KEY: '项目阶段修改成功'}, Const.STATUS_OK


class PhaseListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = Phase.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(PhaseSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        phase = Phase()
        args = parser.parse_args()
        attachments = args.get('attachments')

        if attachments:
            aids = attachments.split(',')

            for aid in aids:
                a = Attachment.query.get(int(aid))
                if a:
                    db.session.expunge(a)
                    pa = PhaseAttachment()
                    pa.attachment = a
                    phase.attachments.append(pa)

            with safe_session(db):
                db.session.add(phase)

        merge(phase, args, ignore=('attachments',))

        with safe_session(db):
            db.session.add(phase)

        return {Const.MESSAGE_KEY: '创建项目阶段成功'}, Const.STATUS_OK
