#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午9:54
# @Author  : Rain
# @Desc    : 测试环境配置文件，部署时*不会*被拷贝到服务器
# @File    : development.py

from .config import Config


class Development(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = '84j548f&$32lkjddflfd(893^'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://apl:Apl123456@rm-2ze9uiue6mo09e0m9o.mysql.rds.aliyuncs.com/apl'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/apl'
    BUCKET_VCODE_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    STS_DURATION_SECONDS = 3600
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
    ADMIN_SESSION_EXPIRE = PERMANENT_SESSION_LIFETIME
    STARTUP_SESSION_EXPIRE = PERMANENT_SESSION_LIFETIME
    SESSION_COOKIE_SECURE = False
