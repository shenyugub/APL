#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午3:33
# @Author  : Rain
# @Desc    : 用户交付物接口
# @File    : PhaseAttachmentResource.py

from flask_restful import Resource, reqparse
from app.models import Const, PhaseAttachment, PhaseAttachmentSchema, Project, AttachmentStatus, ProjectPhase
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from sqlalchemy import or_


parser = reqparse.RequestParser()
parser.add_argument('phase_id', type=int, location='json', store_missing=False)
parser.add_argument('attachment_id', type=int, location='json', store_missing=False)
parser.add_argument('file_url', type=str, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)
parser.add_argument('comment', type=str, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('project_name', type=str, location='args', store_missing=False)
search_parser.add_argument('status', type=str, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)


class PhaseAttachmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, paid):
        pa = PhaseAttachment.query.get_or_404(paid)
        schema = PhaseAttachmentSchema()
        result = schema.dump(pa).data

        return {'pa': result}, Const.STATUS_OK

    def post(self, paid):
        pa = PhaseAttachment.query.get_or_404(paid)
        args = parser.parse_args()
        merge(pa, args)

        with safe_session(db):
            db.session.add(pa)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class PhaseAttachmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        conditions = []
        args = search_parser.parse_args()
        project_name = args.get('project_name')
        status = args.get('status')
        starttime = args.get('starttime')
        endtime = args.get('endtime')

        if project_name:
            projects = Project.query.filter(Project.name.contains(project_name)).all()
            if len(projects) > 0:
                pps = ProjectPhase.query.filter(ProjectPhase.project_id.in_([p.id for p in projects])).all()
                if len(pps) > 0:
                    pass
                # conditions.append(PhaseAttachment.id == project.id)

        if status:
            if status.lower() in [a.value.lower() for a in AttachmentStatus.__members__.values()]:
                conditions.append(PhaseAttachment.status == status)

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) < PhaseAttachment.timestamp < int(endtime))

        pas = PhaseAttachment.query.filter(or_(*conditions)).all()

        # TODO
        # pp = ProjectPhase.query.filter_by(phase_id=pas.phase_id).first()
        #
        #
        # pas.project_name = '' if pp is None else pp.project_id
        # pas.phase_name =
        # pas.attachment_name =

        for pa in pas:
            pa.project_name = '111'
            pa.phase_name = '222'
            pa.attachment_name = '333'

        schema = PhaseAttachmentSchema(many=True)
        result = schema.dump(pas).data

        return {'pas': result}, Const.STATUS_OK

    def post(self):
        pa = PhaseAttachment()
        args = parser.parse_args()
        merge(pa, args)

        with safe_session(db):
            db.session.add(pa)

        return {Const.MESSAGE_KEY: '创建成功'}, Const.STATUS_OK
