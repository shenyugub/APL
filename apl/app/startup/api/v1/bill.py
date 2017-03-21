# -*- coding: utf-8 -*-
from app.models import UserServiceItem, PaginationSchema, \
    UserServiceItemSchema, Const
from flask import current_app
from flask_restful import Resource
from sqlalchemy import and_
from marshmallow import fields

from app.utils.utils import merge, safe_session
from app import user_manager, db
from .parsers import bill_search_parser


class BillHandler(Resource):
    # method_decorators = [user_manager.login_required()]

    def get(self, sid=None):
        if sid is not None:
            schema = UserServiceItemSchema()
            bill = UserServiceItem.query.filter_by(id=sid).first()
            result = schema.dump(bill).data
        else:
            args = bill_search_parser.parse_args()
            usid = args.get('id')
            project_name = args.get('project_name')
            starttime = args.get('starttime')
            endtime = args.get('endtime')
            page = args.get('page')
            per_page = current_app.config['ITEM_COUNT_PER_PAGE']
            conditions = []
            if isinstance(usid, int):
                conditions.append(UserServiceItem.id == usid)
            if project_name:
                conditions.append(UserServiceItem.project_name.contains(project_name))
            if isinstance(starttime, int) and isinstance(endtime, int):
                conditions.append(int(starttime) <= UserServiceItem.timestamp <= int(endtime))
            pagination = UserServiceItem.query.filter(and_(*conditions)).paginate(page, per_page=per_page, error_out=False)
            schema = PaginationSchema()
            schema.declared_fields['items'] = fields.Nested(UserServiceItemSchema, many=True)
            result = schema.dump(pagination).data
        return {Const.RESULT_KEY: result}, Const.STATUS_OK
