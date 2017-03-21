#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/10 下午4:58
# @Author  : Rain
# @Desc    : 用户接口
# @File    : startup_resource.py

from flask_restful import Resource, reqparse
from app.models import Startup, StartupSchema, Const, Industry, PaginationSchema
from app import admin_manager, db
from app.utils.utils import safe_session, merge
import sqlalchemy
from sqlalchemy import and_
from flask import current_app
from marshmallow import fields
from app.exceptions import EmailExistsException


parser = reqparse.RequestParser()

parser.add_argument('password', type=str, location='json', store_missing=False)
parser.add_argument('permissions', type=str, location='json', store_missing=False)
parser.add_argument('type', type=str, location='json', store_missing=False)
parser.add_argument('confirmed', type=bool, default=True, location='json', store_missing=False)
parser.add_argument('initialized', type=bool, default=True, location='json', store_missing=False)
parser.add_argument('active', type=bool, default=True, location='json', store_missing=False)

parser.add_argument('name', type=str, location='json', store_missing=False)
parser.add_argument('email', type=str, location='json', store_missing=False)
parser.add_argument('phone', type=str, location='json', store_missing=False)
parser.add_argument('wechat', type=str, location='json', store_missing=False)
parser.add_argument('company', type=str, location='json', store_missing=False)
parser.add_argument('gender', type=str, location='json', store_missing=False)
parser.add_argument('avatar', type=str, location='json', store_missing=False)
parser.add_argument('resume', type=str, location='json', store_missing=False)

parser.add_argument('company_name', location='json', store_missing=False)
parser.add_argument('company_desc', type=str, location='json', store_missing=False)
parser.add_argument('company_industry', type=str, location='json', store_missing=False)

search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=str, location='args', store_missing=False)
search_parser.add_argument('type', type=str, location='args', store_missing=False)
search_parser.add_argument('name', type=str, location='args', store_missing=False)
search_parser.add_argument('email', type=str, location='args', store_missing=False)
search_parser.add_argument('phone', type=str, location='args', store_missing=False)
search_parser.add_argument('company_industry', type=str, location='args', store_missing=False)
search_parser.add_argument('company_name', type=str, location='args', store_missing=False)
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class StartupResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, uid):

        startup = Startup.query.get_or_404(uid)

        schema = StartupSchema()

        result = schema.dump(startup).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, uid):

        startup = Startup.query.get_or_404(uid)
        base_args = parser.parse_args()
        merge(startup, base_args, ignore=('email',))  #不允许修改 email

        with safe_session(db):
            db.session.add(startup)

        return {Const.MESSAGE_KEY: '修改用户信息成功'}, Const.STATUS_OK


class StartupListResource(Resource):
    # method_decorators = [admin_manager.login_required()]

    def get(self):

        conditions = []

        args = search_parser.parse_args()

        uid = args.get('id')
        name = args.get('name')
        email = args.get('email')
        phone = args.get('phone')
        company_industry = args.get('company_industry')
        company_name = args.get('company_name')
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        if isinstance(uid, int):
            conditions.append(Startup.id == uid)

        if name:
            conditions.append(Startup.name.contains(name))

        if email:
            conditions.append(Startup.email.contains(email))

        if phone:
            conditions.append(Startup.phone.contains(phone))

        if company_industry in Industry.__members__.keys():
            conditions.append(Startup.company_industry == Industry[company_industry])

        if company_name:
                conditions.append(Startup.company_name.contains(company_name))

        pagination = Startup.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)
        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(StartupSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):

        startup = Startup()
        base_args = parser.parse_args()
        merge(startup, base_args)

        try:
            with safe_session(db):
                db.session.add(startup)
        except sqlalchemy.exc.IntegrityError:
            raise EmailExistsException()

        return {Const.MESSAGE_KEY: '创建用户成功'}, Const.STATUS_OK
