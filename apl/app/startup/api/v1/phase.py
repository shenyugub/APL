# -*- coding: utf-8 -*-
from pprint import pprint
from flask import request


from marshmallow import fields
from flask_restful import Resource
from sqlalchemy import and_
from flask import current_app, request

from app import user_manager, db
from app.models import Phase, PhaseSchema, Attachment, PhaseAttachment
from app.utils.utils import safe_session, merge

from .parsers import phase_parser, phase_search_parser


class PhaseHandler(Resource):

    def get(self, pid=None):
        if pid is not None:
            phase = Phase.query.get_or_404(pid)
            phase.atts = []
            for a in phase.attachments:
                phase.atts.append(a.attachment)
            schema = PhaseSchema(exclude=('atts.phase_id',))
            result = schema.dump(phase).data
        else:
            args = phase_search_parser.parse_args()
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            pagination = Phase.query.paginate(page, per_page=per_page, error_out=False)
            schema = PaginationSchema()
            schema.declared_fields['items'] = fields.Nested(PhaseSchema, many=True)
            result = schema.dump(pagination).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self):
        phase = Phase()
        args = phase_parser.parse_args()
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

    def put(self, pid):
        phase = Phase.query.get_or_404(pid)
        args = phase_parser.parse_args()
        merge(phase, args, ignore=('attachments',))

        with safe_session(db):
            db.session.add(phase)

        return {Const.MESSAGE_KEY: '项目阶段修改成功'}, Const.STATUS_OK
