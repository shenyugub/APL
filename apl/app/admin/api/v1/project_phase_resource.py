#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 下午9:10
# @Author  : Rain
# @Desc    : 用户项目阶段接口
# @File    : project_phase_resource.py.py

from app.models import Const, ProjectPhase, ProjectPhaseSchema, PaginationSchema
from app.utils.utils import safe_session, merge
from flask_restful import Resource, reqparse
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('project_id', type=int, location='json', store_missing=False)
parser.add_argument('phase_id', type=int, location='json', store_missing=False)
parser.add_argument('days', type=int, location='json', store_missing=False)
parser.add_argument('status', type=int, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class ProjectPhaseResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, ppid):
        pp = ProjectPhase.query.get_or_404(ppid)

        schema = ProjectPhaseSchema()
        result = schema.dump(pp).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, ppid):
        pp = ProjectPhase.query.get_or_404(ppid)
        args = parser.parse_args()
        merge(pp, args, ignore=('project_id', 'phase_id'))

        with safe_session(db):
            db.session.add(pp)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class ProjectPhaseListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = ProjectPhase.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(ProjectPhaseSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        pp = ProjectPhase()
        args = parser.parse_args()
        merge(pp, args)

        with safe_session(db):
            db.session.add(pp)

        return {Const.MESSAGE_KEY: '创建成功'}, Const.STATUS_OK
