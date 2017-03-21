#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午9:10
# @Author  : Rain
# @Desc    : 用户项目阶段接口
# @File    : project_phase_resource.py.py

from app.models import Const, ProjectPhase, ProjectPhaseSchema
from app.utils.utils import safe_session, merge
from flask_restful import Resource, reqparse
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('project_id', type=int, location='json', store_missing=False)
parser.add_argument('phase_id', type=int, location='json', store_missing=False)
parser.add_argument('days', type=int, location='json', store_missing=False)
parser.add_argument('status', type=int, location='json', store_missing=False)


class ProjectPhaseResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, ppid):
        pp = ProjectPhase.query.get_or_404(ppid)

        # if pp:
        #     pp.attachments = []
        #     for a in pp.phase.attachments:
        #         print(a.attachment)
        #         pp.attachments.append(a.attachment)

        schema = ProjectPhaseSchema()
        result = schema.dump(pp).data

        return {'pp': result}, Const.STATUS_OK

    def post(self, ppid):
        pp = ProjectPhase.query.get_or_404(ppid)
        args = parser.parse_args()
        merge(pp, args)

        with safe_session(db):
            db.session.add(pp)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class ProjectPhaseListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        pps = ProjectPhase.query.all()
        schema = ProjectPhaseSchema(many=True)
        result = schema.dump(pps).data

        return {'pps': result}, Const.STATUS_OK

    def post(self):
        pp = ProjectPhase()
        args = parser.parse_args()
        merge(pp, args)

        with safe_session(db):
            db.session.add(pp)

        return {Const.MESSAGE_KEY: '创建成功'}, Const.STATUS_OK
