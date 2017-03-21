#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午4:14
# @Author  : Rain
# @Desc    : 投资人对项目的点评接口
# @File    : comment_resource.py

from flask_restful import reqparse, Resource
from app.models import Comment, CommentSchema, Const
from app.utils.utils import merge, safe_session
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('project_id', type=int, location='json', store_missing=False)
parser.add_argument('author_id', type=int, location='json', store_missing=False)
parser.add_argument('content', type=str, location='json', store_missing=False)
parser.add_argument('timestamp', type=int, location='json', store_missing=False)


class CommentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, cid):
        comment = Comment.query.get_or_404(cid)
        comment.project_name = comment.project.name
        comment.author_name = comment.author.name

        schema = CommentSchema()
        result = schema.dump(comment).data

        return {'comment': result}, Const.STATUS_OK

    def post(self, cid):
        comment = Comment.query.get_or_404(cid)
        args = parser.parse_args()
        merge(comment, args)

        with safe_session(db):
            db.session.add(comment)

        return {Const.MESSAGE_KEY: '点评修改成功'}, Const.STATUS_OK


class CommentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        comments = Comment.query.all()
        for comment in comments:
            comment.project_name = comment.project.name
            comment.author_name = comment.author.name

        schema = CommentSchema(many=True)
        result = schema.dump(comments).data

        return {'comments': result}, Const.STATUS_OK

    def post(self):

        comment = Comment()
        args = parser.parse_args()
        merge(comment, args)

        with safe_session(db):
            db.session.add(comment)

        return {Const.MESSAGE_KEY: '点评发布成功'}, Const.STATUS_OK
