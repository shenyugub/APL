#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/6 下午5:11
# @Author  : Rain
# @Desc    : 项目接口
# @File    : project_resource.py

from flask_restful import Resource,  reqparse
from app import admin_manager, db
from app.models import Project, ProjectSchema, Const, Industry, PaginationSchema
from app.utils.utils import safe_session, merge
from sqlalchemy import and_
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('owner_id', type=int, location='json', store_missing=False)
parser.add_argument('icon_url', type=str, location='json', store_missing=False)
parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('advantage', type=str, location='json', store_missing=False)
parser.add_argument('industry', type=str, location='json', store_missing=False)

parser.add_argument('company_phase', type=str, location='json', store_missing=False)
parser.add_argument('financing_sum', type=int, location='json', store_missing=False)
parser.add_argument('bp_url', type=str, location='json', store_missing=False)
parser.add_argument('duration', type=int, location='json', store_missing=False)
parser.add_argument('financing_status', type=str, location='json', store_missing=False)

parser.add_argument('deadline', type=str, location='json', store_missing=False)
parser.add_argument('contact_name', type=str, location='json', store_missing=False)
parser.add_argument('contact_phone', type=str, location='json', store_missing=False)
parser.add_argument('contact_email', type=str, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=int, location='args', store_missing=False)
search_parser.add_argument('name', type=str, location='args', store_missing=False)
search_parser.add_argument('contact_name', type=str, location='args', store_missing=False)
search_parser.add_argument('industry', type=str, location='args', store_missing=False)
search_parser.add_argument('phase_index', type=int, location='args', store_missing=False)
search_parser.add_argument('contact_phone', type=str, location='args', store_missing=False)
search_parser.add_argument('starttime', type=str, location='args', store_missing=False)
search_parser.add_argument('endtime', type=str, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class ProjectResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, pid):
        project = Project.query.get_or_404(pid)

        schema = ProjectSchema(exclude=('comments.project_id', 'phases.project_id'))
        result = schema.dump(project).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, pid):

        project = Project.query.get_or_404(pid)
        args = parser.parse_args()
        merge(project, args, ignore=('owner_id',))

        with safe_session(db):
            db.session.add(project)

        return {Const.MESSAGE_KEY: '项目修改成功'}, Const.STATUS_OK


class ProjectListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        pid = args.get('id')
        name = args.get('name')
        contact_name = args.get('contact_name')
        industry = args.get('industry')
        phase_index = args.get('phase_index')
        contact_phone = args.get('contact_phone')
        starttime = args.get('starttime')
        endtime = args.get('endtime')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        conditions = []

        if isinstance(pid, int):
            conditions.append(Project.id == pid)

        if name:
            conditions.append(Project.name.contains(name))

        if contact_name:
            conditions.append(Project.contact_name.contains(contact_name))

        if industry in Industry.__members__.keys():
            conditions.append(Project.industry == Industry[industry])

        if phase_index:
            conditions.append(Project.phase_index == phase_index)

        if contact_phone:
            conditions.append(Project.contact_phone.contains(contact_phone))

        if isinstance(starttime, int) and isinstance(endtime, int):
            conditions.append(int(starttime) <= Project.gmt_create <= int(endtime))

        pagination = Project.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(ProjectSchema, many=True)  # , exclude=('comments.project_id', 'phases.project_id'))

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        project = Project()
        args = parser.parse_args()
        merge(project, args)

        with safe_session(db):
            db.session.add(project)

        return {Const.MESSAGE_KEY: '创建项目成功'}, Const.STATUS_OK
