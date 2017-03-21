#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/21 上午11:53
# @Author  : Rain
# @Desc    :
# @File    : __init__.py.py

from flask import Blueprint

investor = Blueprint('investor', __name__)

from .api.v1 import api_v1
