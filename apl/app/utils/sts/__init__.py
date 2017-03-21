#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/9 下午1:46
# @Author  : Rain
# @Desc    : 阿里云 RAM 服务获取临时授权的工具类
# @File    : __init__.py.py


import base64
import hmac
from hashlib import sha1
import urllib.parse
import time
import uuid
import requests
import json
import oss2
from flask import current_app


config = {
    'ACCESS_KEY': 'LTAI04knfX7WRTmj',
    'ACCESS_KEY_SECRET': 'MjtDGgfgtfTkb05mlHc0IjDo23hN9G',
    'ROLE_ARN': 'acs:ram::1874184839631583:role/uploader',
    'ACCESS_URL': 'https://sts.aliyuncs.com',
}


class AliyunSTS(object):
    def __init__(self):
        self.access_id = config.get('ACCESS_KEY')
        self.access_secret = config.get('ACCESS_KEY_SECRET')
        self.url = config.get('ACCESS_URL')


def sign(access_key_secret, parameter):
    sorted_parameters = sorted(parameter.items(), key=lambda p: p[0])
    canonicalized_query_string = ''
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&' + percent_encode(k) + '=' + percent_encode(v)
    string_to_sign = 'GET&%2F&' + percent_encode(canonicalized_query_string[1:])
    hash_str = hmac.new(bytes((access_key_secret + "&").encode("utf-8")), string_to_sign.encode('utf-8'), sha1)
    return base64.encodebytes(hash_str.digest()).strip()


def percent_encode(encode_str):
    encode_str = str(encode_str)
    result = urllib.parse.quote(encode_str.encode('utf-8'), '')
    result = result.replace('+', '%20')
    result = result.replace('*', '%2A')
    result = result.replace('%7E', '~')
    return result


def make_url(secret, url, parameters):

    signature = sign(secret, parameters)
    parameters['Signature'] = signature

    u = url + "/?" + urllib.parse.urlencode(parameters)
    return u


class STSToken(object):
    def __init__(self):
        self.access_key_id = ''
        self.access_key_secret = ''
        self.expiration = 0
        self.security_token = ''


def request_sts_token(uid):

    try:

        sts = AliyunSTS()

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        data = {
            'Action': 'AssumeRole',
            'RoleArn': config.get('ROLE_ARN'),
            'RoleSessionName': str(uid),
            'DurationSeconds': current_app.config.get('STS_DURATION_SECONDS'),
            'Format': 'JSON',
            'Version': '2015-04-01',
            'AccessKeyId': sts.access_id,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }

        url = make_url(sts.access_secret, sts.url, data)

        response = requests.get(url)
        if response.status_code != 200:
            return None
    except requests.Timeout:
        return None

    content = json.loads(response.text)

    token = STSToken()

    token.access_key_id = content['Credentials']['AccessKeyId']
    token.access_key_secret = content['Credentials']['AccessKeySecret']
    token.expiration = content['Credentials']['Expiration']
    token.security_token = content['Credentials']['SecurityToken']

    print('AccessKeyId = {}\n AccessKeySecret = {}\n Expiration = {}\n SecurityToken = {}\n'.format(token.access_key_id, token.access_key_secret, token.expiration, token.security_token))

    return token


def get_file_url(server_name, local_file):
    sts_token = request_sts_token('kevin')

    auth = oss2.StsAuth(sts_token.access_key_id, sts_token.access_key_secret, sts_token.security_token)
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'apl-docs')
    url = bucket.sign_url('GET', server_name, 1800, params={"response-content-disposition": "attachment; filename=%s" % local_file})
    return url

