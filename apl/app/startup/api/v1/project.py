# -*- coding: utf-8 -*-
from pprint import pprint
from flask import request


from marshmallow import fields
from flask_restful import Resource
from sqlalchemy import and_
from flask import current_app, request

from app import user_manager, db
from app.models import Project, ProjectSchema, Const, Industry, Phase, ProjectPhase, PaginationSchema
from app.utils.utils import safe_session, merge

from .parsers import project_search_parser, project_create_parser


class ProjectHandler(Resource):

    method_decorators = [user_manager.login_required()]

    def get(self, pid=None):
        user = user_manager.current_user
        if pid is not None:
            project = Project.query.filter_by(owner_id=user.id, id=pid).first()
            if project is not None:
                for phase in project.phases:
                    phase.phase_name = phase.phase.name
                schema = ProjectSchema(
                    exclude=('comments.project_id', 'phases.project_id')
                )
                result = schema.dump(project).data
            else:
                result = {}
        else:
            args = project_search_parser.parse_args()
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

            conditions = [Project.owner_id == user.id, ]
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
                conditions.append(
                    Project.contact_phone.contains(contact_phone)
                )
            if isinstance(starttime, int) and isinstance(endtime, int):
                conditions.append(
                    int(starttime) <= Project.gmt_create <= int(endtime)
                )
            pagination = Project.query.filter(and_(*conditions)).paginate(
                page, per_page=per_page, error_out=False
            )
            schema = PaginationSchema()
            schema.declared_fields['items'] = fields.Nested(ProjectSchema, many=True)
            result = schema.dump(pagination).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self):
        project = Project()
        args = project_create_parser.parse_args()
        try:
            merge(project, args)
            with safe_session(db):
                db.session.add(project)
        except Exception as e:
            print(e)
            return {Const.MESSAGE_KEY: '接口请失败求'}, Const.STATUS_ERROR
        return {Const.MESSAGE_KEY: '创建项目成功'}, Const.STATUS_OK

    def put(self, pid):
        project = Project.query.filter_by(id=pid).first()
        if project:
            ret = {Const.MESSAGE_KEY: '找不到项目'}, Const.STATUS_NOTFOUND
            try:
                args = project_create_parser.parse_args()
                merge(project, args, ignore=('owner_id',))
                with safe_session(db):
                    db.session.add(project)
                ret = {Const.MESSAGE_KEY: '项目修改成功'}, Const.STATUS_OK
            except Exception as e:
                print(str(e))
                ret = {Const.MESSAGE_KEY: '项目修改失败'}, Const.STATUS_ERROR
        else:
            ret = {Const.MESSAGE_KEY: '项目不存在'}, Const.STATUS_NOTFOUND
        return ret

    def delete(self):
        raise Exception("Delete method is not allow")
