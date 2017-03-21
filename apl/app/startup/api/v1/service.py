# -*- coding: utf-8 -*-
from app.models import ServiceItemCategory, ServiceItemCategorySchema,\
    Const, PaginationSchema, ServiceItem, ServiceItemSchema,\
    UserServiceItem, UserServiceItemSchema, Project, CustomServiceItem,\
    CustomServiceItemSchema, ProjectPhase
from flask_restful import Resource
from app.utils.utils import merge, safe_session
from app import user_manager, db
from flask import current_app
from marshmallow import fields

from .parsers import service_category_parser, service_category_search_parser, \
            service_item_search_parser, user_service_item_parser, \
            custom_service_item_parser, custom_service_list_parser, \
            user_service_list_parser


class ServiceHandler(Resource):
    # method_decorators = [user_manager.login_required()]

    def get(self, sid=None):
        if sid is not None:
            schema = ServiceItemSchema()
            service = ServiceItem.query.get_or_404(sid)
            result = schema.dump(service).data
        else:
            schema = PaginationSchema()
            args = service_item_search_parser.parse_args()
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            pagination = ServiceItem.query.paginate(
                page, per_page=per_page, error_out=False)
            schema.declared_fields['items'] = fields.Nested(ServiceItemSchema, many=True)
            result = schema.dump(pagination).data
            return {Const.RESULT_KEY: result}, Const.STATUS_OK


class UserServiceHandler(Resource):

    def get(self, usiid=None):
        if usiid is None:
            user = user_manager.current_user
            args = user_service_list_parser.parse_args()
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            schema = PaginationSchema()
            schema.declared_fields['items'] = fields.Nested(UserServiceItemSchema, many=True)
            raw_projects_ids = Project.query.filter_by(
                owner_id=1).values(Project.id)
            try:
                projects_ids = list(zip(*raw_projects_ids))[0]
            except Exception as e:
                print(e)
                projects_ids = []
            try:
                raw_ph_ids = ProjectPhase.query.filter(
                    ProjectPhase.project_id.in_(projects_ids)).values(
                        ProjectPhase.id
                )
                ph_ids = list(zip(*raw_ph_ids))[0]
            except Exception as e:
                ph_ids = []
            user_service_items = UserServiceItem.query.filter(
                UserServiceItem.ppid.in_(ph_ids)).paginate(
                    page, per_page=per_page, error_out=False
            )
            result = schema.dump(user_service_items).data
        else:
            item = UserServiceItem.query.get_or_404(usiid)
            schema = UserServiceItemSchema()
            result = schema.dump(item).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self):
        args = user_service_item_parser.parse_args()
        us = UserServiceItem()
        merge(us, args)
        with safe_session(db):
            db.session.add(us)
        return {Const.MESSAGE_KEY: '用户服务申请创建成功'}, Const.STATUS_OK

    def put(self, usiid):
        usi = UserServiceItem.query.get_or_404(usiid)
        args = parser.parse_args()
        merge(usi, args, ignore=('ppid', 'service_id'))
        with safe_session(db):
            db.session.add(usi)

        return {Const.MESSAGE_KEY: '用户服务申请修改成功'}, Const.STATUS_OK


class CustomServiceHandler(Resource):

    def get(self, csiid=None):
        user = user_manager.current_user
        if csiid is None:
            args = custom_service_list_parser.parse_args()
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            schema = PaginationSchema()
            schema.declared_fields['items'] = fields.Nested(CustomServiceItemSchema, many=True)
            raw_projects_ids = Project.query.filter_by(
                owner_id=user.id).values(Project.id)
            try:
                projects_ids = list(zip(*raw_projects_ids))[0]
            except Exception as e:
                print(e)
                projects_ids = []
            try:
                raw_ph_ids = ProjectPhase.query.filter(
                    ProjectPhase.project_id.in_(projects_ids)).values(
                        ProjectPhase.id
                )
                ph_ids = list(zip(*raw_ph_ids))[0]
            except Exception as e:
                ph_ids = []
            custom_service_items = CustomServiceItem.query.filter(
                CustomServiceItem.ppid.in_(ph_ids)).paginate(
                    page, per_page=per_page, error_out=False
            )
            result = schema.dump(custom_service_items).data
        else:
            item = CustomServiceItem.query.get_or_404(csiid)
            schema = CustomServiceItemSchema()
            result = schema.dump(item).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self):
        args = custom_service_item_parser.parse_args()
        cs = CustomServiceItem()
        try:
            merge(cs, args)
            with safe_session(db):
                db.session.add(cs)
        except Exception as e:
            return {Const.MESSAGE_KEY: '接口请求错误'}, Const.STATUS_ERROR
        return {Const.MESSAGE_KEY: '用户自定义服务申请创建成功'}, Const.STATUS_OK

    def put(self, csiid):
        csi = CustomServiceItem.query.get_or_404(csiid)
        args = custom_service_item_parser.parse_args()
        merge(usi, args)
        with safe_session(db):
            db.session.add(csi)
        return {Const.MESSAGE_KEY: '用户服务申请修改成功'}, Const.STATUS_OK


class ServiceCategoryHandler(Resource):
    # method_decorators = [user_manager.login_required()]

    def get(self, scid=None):
        if scid is not None:
            schema = ServiceItemCategorySchema()
            sc = ServiceItemCategory.query.get_or_404(scid)
            result = schema.dump(sc).data
        else:
            schema = PaginationSchema()
            args = service_category_search_parser.parse_args()
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            pagination = ServiceItemCategory.query.paginate(page, per_page=per_page, error_out=False)
            schema.declared_fields['items'] = fields.Nested(ServiceItemCategorySchema, many=True)
            result = schema.dump(pagination).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK
