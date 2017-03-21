#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午9:54
# @Author  : Rain
# @Desc    : 基础配置文件，部署时会被自动拷贝到服务器
# @File    : config.py

from redis import Redis


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    SQLALCHEMY_POOL_TIMEOUT = 900
    SQLALCHEMY_POOL_RECYCLE = 900
    SQLALCHEMY_POOL_SIZE = 300
    SQLALCHEMY_MAX_OVERFLOW = 50
    ITEM_COUNT_PER_PAGE = 10
    SESSION_TYPE = 'redis'
    REDIS_SECRET = r'''%yz=)S/OyE?uvTEj'''
    SESSION_REDIS = Redis(host='apl.apluslabs.com', password=REDIS_SECRET)
    SESSION_COOKIE_NAME = 'apl'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_USE_SIGNER = True
    SESSION_FILE_THRESHOLD = 10000


def init_app(app):
    pass
