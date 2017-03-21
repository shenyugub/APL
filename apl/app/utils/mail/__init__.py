#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/8 上午9:48
# @Author  : Rain
# @Desc    : 发送阿里云邮件的工具类
# @File    : __init__.py.py

import base64
import hmac
from hashlib import sha1
import urllib.parse
import time
import uuid
import requests


config = {
    'ACCESS_KEY': 'LTAIlc6aqV7yfOn5',
    'ACCESS_KEY_SECRET': '1VXgjUXBbWdiiWEKBDDaq2kjlKm4fe',
    'ACCESS_URL': 'https://dm.aliyuncs.com',
    'ACCOUNT_NAME': 'admin@apl.mail.apluslabs.com',
    'REPLY_TO_ADDRESS': True,
    'ADDRESS_TYPE': 0,  # 取值范围0~1: 0为随机账号(推荐,可以更好的统计退信情况);1为发信地址
    'FROM_ALIAS': 'APL Admin',
}


class AliyunMail(object):
    def __init__(self):
        self.access_id = config.get('ACCESS_KEY')
        self.access_secret = config.get('ACCESS_KEY_SECRET')
        self.url = config.get('ACCESS_URL')

    def sign(self, access_key_secret, parameter):
        sorted_parameters = sorted(parameter.items(), key=lambda p: p[0])
        canonicalized_query_string = ''
        for (k, v) in sorted_parameters:
            canonicalized_query_string += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        string_to_sign = 'GET&%2F&' + self.percent_encode(canonicalized_query_string[1:])
        hash_str = hmac.new(bytes((access_key_secret + "&").encode("utf-8")), string_to_sign.encode('utf-8'), sha1)
        return base64.encodebytes(hash_str.digest()).strip()

    @staticmethod
    def percent_encode(encode_str):
        encode_str = str(encode_str)
        result = urllib.parse.quote(encode_str.encode('utf-8'), '')
        result = result.replace('+', '%20')
        result = result.replace('*', '%2A')
        result = result.replace('%7E', '~')
        return result

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        parameters = {
            'Format': 'JSON',
            'Version': '2015-11-23',
            'AccessKeyId': self.access_id,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': timestamp,
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
        }

        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature
        url = self.url + "/?" + urllib.parse.urlencode(parameters)
        return url


def send(to, subject, html_body, text_body=''):
    try:

        aliyun = AliyunMail()

        data = {
            'Action': 'SingleSendMail',
            'AccountName': config.get('ACCOUNT_NAME'),
            'ReplyToAddress': config.get('REPLY_TO_ADDRESS'),
            'AddressType': config.get('ADDRESS_TYPE'),
            'ToAddress': to,
            'FromAlias': config.get('FROM_ALIAS'),
            'Subject': subject,
            'TextBody': text_body,
            'HtmlBody': html_body,
        }

        url = aliyun.make_url(data)
        response = requests.get(url)
        if response.status_code != 200:
            return False
    except requests.Timeout:
        return False

    return True
