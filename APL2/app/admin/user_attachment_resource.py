#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/11 下午4:14
# @Author  : Rain
# @Desc    : 用户交付物接口
# @File    : comment_resource.py

from flask_restful import reqparse, Resource
from app.models import UserAttachment, UserAttachmentSchema, Const, ProjectPhase, Attachment
from app.utils.utils import merge, safe_session
from app import admin_manager, db


parser = reqparse.RequestParser()
parser.add_argument('ppid', type=int, location='json', store_missing=False)
parser.add_argument('attachment_id', type=int, location='json', store_missing=False)
parser.add_argument('status', type=str, location='json', store_missing=False)
parser.add_argument('url', type=str, location='json', store_missing=False)
parser.add_argument('comment', type=str, location='json', store_missing=False)


class UserAttachmentResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self, uaid):
        attachment = UserAttachment.query.get_or_404(uaid)
        attachment.project_name = ProjectPhase.query.get(attachment.ppid).project.name
        attachment.attachment_name = Attachment.query.get(attachment.attachment_id).name

        schema = UserAttachmentSchema()
        result = schema.dump(attachment).data

        return {'attachment': result}, Const.STATUS_OK

    def post(self, uaid):
        attachment = UserAttachment.query.get_or_404(uaid)
        args = parser.parse_args()
        merge(attachment, args)

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '交付物修改成功'}, Const.STATUS_OK


class UserAttachmentListResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):
        attachments = UserAttachment.query.all()
        for attachment in attachments:

            if attachment.ppid:
                pp = ProjectPhase.query.get(attachment.ppid)
                if pp and pp.project:
                    attachment.project_name = pp.project.name

            if attachment.attachment_id:
                a = Attachment.query.get(attachment.attachment_id)
                if a:
                    attachment.attachment_name = a.name

        schema = UserAttachmentSchema(many=True)
        result = schema.dump(attachments).data

        return {'attachments': result}, Const.STATUS_OK

    def post(self):

        attachment = UserAttachment()
        args = parser.parse_args()

        merge(attachment, args)

        with safe_session(db):
            db.session.add(attachment)

        return {Const.MESSAGE_KEY: '交付物发布成功'}, Const.STATUS_OK
