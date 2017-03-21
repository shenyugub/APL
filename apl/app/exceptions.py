#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 下午1:36
# @Author  : Rain
# @Desc    : 异常类
# @File    : exceptions.py

from app.models import Const


# 根据flask-restful的文档和源码，当 DEBUG=True 时，不会返回正确的错误处理数据(我们预定义的json)，而是跳转到出错页面
# http://stackoverflow.com/questions/21638922/custom-error-message-json-object-with-flask-restful


errors = {
    'EmailExistsException': {
        'message': "创建用户失败，该邮箱地址已存在",
        'status': Const.STATUS_ERROR,
    },
    'IllegalPermissionValueException': {
        'message': "非法权限值",
        'status': Const.STATUS_ERROR,
    },
    'NotFound': {
        'message': "找不到请求的资源",
        'status': Const.STATUS_NOTFOUND,
    },
    'Exception': {
        'message': "系统错误",
        'status': 500,
    },
}


class EmailExistsException(Exception):
    pass


class IllegalPermissionValueException(Exception):
    pass
