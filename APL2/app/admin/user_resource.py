#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/10 下午4:58
# @Author  : Rain
# @Desc    : 用户接口
# @File    : user_resource.py

from flask_restful import Resource, reqparse
from app.models import User, UserType, StartupSchema, InvestorSchema, Const, Industry
from app import admin_manager, db
from app.utils.utils import safe_session, merge
import sqlalchemy
from sqlalchemy import or_


base_parser = reqparse.RequestParser()

base_parser.add_argument('password', type=str, location='json', store_missing=False)
base_parser.add_argument('permissions', type=str, location='json', store_missing=False)
base_parser.add_argument('type', type=str, location='json', store_missing=False)
base_parser.add_argument('confirmed', type=bool, default=True, location='json', store_missing=False)
base_parser.add_argument('initialized', type=bool, default=True, location='json', store_missing=False)
base_parser.add_argument('active', type=bool, default=True, location='json', store_missing=False)

base_parser.add_argument('name', type=str, location='json', store_missing=False)
base_parser.add_argument('email', type=str, location='json', store_missing=False)
base_parser.add_argument('phone', type=str, location='json', store_missing=False)
base_parser.add_argument('wechat', type=str, location='json', store_missing=False)
base_parser.add_argument('company', type=str, location='json', store_missing=False)
base_parser.add_argument('gender', type=str, location='json', store_missing=False)
base_parser.add_argument('avatar', type=str, location='json', store_missing=False)
base_parser.add_argument('resume', type=str, location='json', store_missing=False)

startup_parser = reqparse.RequestParser()
startup_parser.add_argument('company_name', location='json', store_missing=False)
startup_parser.add_argument('company_desc', type=str, location='json', store_missing=False)
startup_parser.add_argument('company_industry', type=str, location='json', store_missing=False)

investor_parser = reqparse.RequestParser()
investor_parser.add_argument('interested', type=str, location='json', store_missing=False)
investor_parser.add_argument('invest_role', type=str, location='json', store_missing=False)
investor_parser.add_argument('investment_min', type=int, location='json', store_missing=False)
investor_parser.add_argument('investment_max', type=int, location='json', store_missing=False)
investor_parser.add_argument('invest_phase', type=str, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('id', type=str, location='args', store_missing=False)
search_parser.add_argument('type', type=str, location='args', store_missing=False)
search_parser.add_argument('name', type=str, location='args', store_missing=False)
search_parser.add_argument('email', type=str, location='args', store_missing=False)
search_parser.add_argument('phone', type=str, location='args', store_missing=False)
search_parser.add_argument('company_industry', type=str, location='args', store_missing=False)
search_parser.add_argument('company_name', type=str, location='args', store_missing=False)


class UserResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, uid):

        user = User.query.get_or_404(uid)

        if user.type == UserType.Investor:
            schema = InvestorSchema()
        else:
            schema = StartupSchema()

        result = schema.dump(user).data

        return {'user': result}, Const.STATUS_OK

    def post(self, uid):

        user = User.query.get_or_404(uid)

        base_args = base_parser.parse_args()

        merge(user, base_args, ignore=('type', 'email'))  #不允许修改 type 和 email

        if user.type == UserType.Investor:
            investor_args = investor_parser.parse_args()
            merge(user, investor_args)

        else:
            startup_args = startup_parser.parse_args()
            merge(user, startup_args)

        with safe_session(db):
            db.session.add(user)

        return {Const.MESSAGE_KEY: '修改用户信息成功'}, Const.STATUS_OK


class UserListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        conditions = []

        args = search_parser.parse_args()

        t = args.get('type')
        uid = args.get('id')
        name = args.get('name')
        email = args.get('email')
        phone = args.get('phone')
        company_industry = args.get('company_industry')
        company_name = args.get('company_name')

        if t:
            if t in UserType.__members__.keys():
                conditions.append(User.type == UserType[t])

        if isinstance(uid, int):
            conditions.append(User.id == uid)

        if name:
            conditions.append(User.name == name)

        if email:
            conditions.append(User.email == email)

        if phone:
            conditions.append(User.phone == phone)

        if company_industry:
            if company_industry in Industry.__members__.keys():
                conditions.append(User.company_industry == Industry[company_industry])

        if company_name:
                conditions.append(User.company_name == company_name)

        users = User.query.filter(or_(*conditions)).all()

        result = []
        for user in users:

            schema = StartupSchema()

            if user.type == UserType.Investor:
                schema = InvestorSchema()

            result.append(schema.dump(user).data)

        return {'users': result}, Const.STATUS_OK

    def post(self):

        user = User()
        base_args = base_parser.parse_args()
        merge(user, base_args)

        if user.type == UserType.Investor:
            investor_args = investor_parser.parse_args()
            merge(user, investor_args)
        else:
            startup_args = startup_parser.parse_args()
            merge(user, startup_args)

        try:
            with safe_session(db):
                db.session.add(user)
        except sqlalchemy.exc.IntegrityError as e:
            print('create user error:', e)
            return {Const.MESSAGE_KEY: '创建用户失败，该邮箱已存在'}, Const.STATUS_ERROR

        return {Const.MESSAGE_KEY: '创建用户成功'}, Const.STATUS_OK
