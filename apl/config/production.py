#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午9:54
# @Author  : Rain
# @Desc    : 生产环境配置文件，部署时会被自动拷贝到服务器
# @File    : production.py


from .config import Config


class Production(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = '&*y32hkds8ih^%3hkjhsd8%8098432k78'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://server:2Uz3e7yk-mwwdhio^s2y75dj@rm-2ze9uiue6mo09e0m9.mysql.rds.aliyuncs.com/apl'
    BUCKET_VCODE_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
    PERMANENT_SESSION_LIFETIME = 1800
    STS_DURATION_SECONDS = PERMANENT_SESSION_LIFETIME
    SESSION_COOKIE_SECURE = True
