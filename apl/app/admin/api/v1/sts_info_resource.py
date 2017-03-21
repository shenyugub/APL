#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/17 下午12:26
# @Author  : Rain
# @Desc    : 获取阿里云 RAM 临时授权的接口
# @File    : sts_info_resource.py

from flask import jsonify
from app.utils.sts import request_sts_token
from app.utils.utils import get_iso_8601, get_sign_policy
from app import admin_manager
from flask_restful import Resource
import time
import json
import base64
import uuid


class STSInfoResource(Resource):
    method_decorators = [admin_manager.login_required()]

    def get(self):

        now = int(time.time())
        expire_syncpoint = now + 1800
        expire = get_iso_8601(expire_syncpoint)

        policy_dict = dict()
        policy_dict["expiration"] = expire
        condition_array = []
        array_item = list()
        array_item.append("content-length-range")
        array_item.append(0)
        array_item.append(104857600)
        condition_array.append(array_item)

        policy_dict["conditions"] = condition_array

        policy = json.dumps(policy_dict).strip()
        policy_encode = base64.b64encode(bytes(policy, 'utf-8'))

        sts = request_sts_token('rain')

        signature = get_sign_policy(sts.access_key_secret, policy_encode)

        callback_dict = dict()
        callback_dict["callbackUrl"] = "https://apl.apluslabs.com/after_upload"
        callback_dict["callbackBody"] = "bucket=${bucket}&object=${object}&etag=${etag}&size=${size}&mimeType=${mimeType}&filename=${x:filename}&uid=${x:uid}"
        callback_dict["callbackBodyType"] = "application/x-www-form-urlencoded"
        callback_param = json.dumps(callback_dict).strip()
        base64_callback_body = base64.b64encode(bytes(callback_param, 'utf-8'))

        result = dict()
        result['OSSAccessKeyId'] = sts.access_key_id
        result['x-oss-security-token'] = sts.security_token
        result['policy'] = policy_encode.decode()
        result['Signature'] = signature.decode()
        result['key'] = str(uuid.uuid1()).replace('-', '')
        result['success_action_status'] = '201'
        result['callback'] = base64_callback_body.decode()
        result['x:uid'] = 1
        result['x:filename'] = ''

        return jsonify(result)
