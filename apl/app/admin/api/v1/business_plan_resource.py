#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午5:38
# @Author  : Rain
# @Desc    : BP 接口
# @File    : business_plan_resource.py

from flask_restful import Resource, reqparse
from app.models import BusinessPlan, BusinessPlanSchema, Const, PaginationSchema
from app.utils.utils import safe_session, merge
from app import admin_manager, db
from flask import current_app
from marshmallow import fields


parser = reqparse.RequestParser()
parser.add_argument('timestamp', type=str, location='json', store_missing=False)
parser.add_argument('project_name', type=str, location='json', store_missing=False)
parser.add_argument('company_name', type=str, location='json', store_missing=False)
parser.add_argument('financing_sum', type=int, location='json', store_missing=False)
parser.add_argument('valuation', type=int, location='json', store_missing=False)
parser.add_argument('description', type=str, location='json', store_missing=False)
parser.add_argument('contact', type=str, location='json', store_missing=False)
parser.add_argument('contact_title', type=str, location='json', store_missing=False)
parser.add_argument('contact_phone', type=str, location='json', store_missing=False)
parser.add_argument('employees', type=str, location='json', store_missing=False)
parser.add_argument('start_from', type=str, location='json', store_missing=False)
parser.add_argument('city', type=str, location='json', store_missing=False)
parser.add_argument('investors', type=int, location='json', store_missing=False)
parser.add_argument('organization', type=str, location='json', store_missing=False)
parser.add_argument('source', type=str, location='json', store_missing=False)
parser.add_argument('industry', type=str, location='json', store_missing=False)
parser.add_argument('tags', type=str, location='json', store_missing=False)
parser.add_argument('comment', type=str, location='json', store_missing=False)

parser.add_argument('full_time', type=str, location='json', store_missing=False)
parser.add_argument('ceo', type=str, location='json', store_missing=False)
parser.add_argument('cto', type=str, location='json', store_missing=False)
parser.add_argument('cmo', type=str, location='json', store_missing=False)
parser.add_argument('industry_resource', type=str, location='json', store_missing=False)
parser.add_argument('stock_structure', type=str, location='json', store_missing=False)
parser.add_argument('team_desc', type=str, location='json', store_missing=False)

parser.add_argument('market_rate', type=str, location='json', store_missing=False)
parser.add_argument('market_capacity', type=str, location='json', store_missing=False)
parser.add_argument('market_proficiency', type=str, location='json', store_missing=False)
parser.add_argument('rival', type=str, location='json', store_missing=False)
parser.add_argument('pain_point', type=str, location='json', store_missing=False)
parser.add_argument('our_resource', type=str, location='json', store_missing=False)

parser.add_argument('product_status', type=str, location='json', store_missing=False)
parser.add_argument('business_mode', type=str, location='json', store_missing=False)
parser.add_argument('main_income', type=str, location='json', store_missing=False)
parser.add_argument('income_status', type=str, location='json', store_missing=False)
parser.add_argument('dest_customers', type=str, location='json', store_missing=False)
parser.add_argument('customers_resource', type=str, location='json', store_missing=False)
parser.add_argument('core_tech', type=str, location='json', store_missing=False)
parser.add_argument('tech_evaluation', type=str, location='json', store_missing=False)
parser.add_argument('core_resource', type=str, location='json', store_missing=False)
parser.add_argument('recent_plan', type=str, location='json', store_missing=False)
parser.add_argument('future_plan', type=str, location='json', store_missing=False)
parser.add_argument('future_aim', type=str, location='json', store_missing=False)

parser.add_argument('needs_desc', type=str, location='json', store_missing=False)
parser.add_argument('needs_support', type=str, location='json', store_missing=False)
parser.add_argument('financing_plan', type=str, location='json', store_missing=False)
parser.add_argument('potential_income', type=str, location='json', store_missing=False)
parser.add_argument('risk', type=str, location='json', store_missing=False)
parser.add_argument('risk_detail', type=str, location='json', store_missing=False)

parser.add_argument('score_needs', type=int, location='json', store_missing=False)
parser.add_argument('score_industry', type=int, location='json', store_missing=False)
parser.add_argument('score_product', type=int, location='json', store_missing=False)
parser.add_argument('score_team', type=int, location='json', store_missing=False)
parser.add_argument('score_resource', type=int, location='json', store_missing=False)
parser.add_argument('score_mode', type=int, location='json', store_missing=False)
parser.add_argument('score_evaluation', type=int, location='json', store_missing=False)
parser.add_argument('score_risk', type=int, location='json', store_missing=False)
parser.add_argument('bp_url', type=int, location='json', store_missing=False)


search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int, default=1, location='args', store_missing=True)


class BusinessPlanResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, bid):
        bp = BusinessPlan.query.get_or_404(bid)
        schema = BusinessPlanSchema()
        result = schema.dump(bp).data

        return {Const.RESULT_KEY: result}, Const.STATUS_OK

    def post(self, bid):
        bp = BusinessPlan.query.get_or_404(bid)
        args = parser.parse_args()
        merge(bp, args)

        with safe_session(db):
            db.session.add(bp)

        return {Const.MESSAGE_KEY: '修改成功'}, Const.STATUS_OK


class BusinessPlanListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        args = search_parser.parse_args()
        page = args.get('page')
        per_page = current_app.config['ITEM_COUNT_PER_PAGE']

        pagination = BusinessPlan.query.paginate(page, per_page=per_page, error_out=False)

        schema = PaginationSchema()
        schema.declared_fields['items'] = fields.Nested(BusinessPlanSchema, many=True)

        data = schema.dump(pagination).data

        return {Const.RESULT_KEY: data}, Const.STATUS_OK

    def post(self):
        bp = BusinessPlan()
        args = parser.parse_args()
        merge(bp, args)

        with safe_session(db):
            db.session.add(bp)

        return {Const.MESSAGE_KEY: '创建成功'}, Const.STATUS_OK
