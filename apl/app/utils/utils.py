#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午9:54
# @Author  : Rain
# @Desc    : 工具类
# @File    : utils.py

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import oss2
import uuid
import tempfile
import base64
import re
import datetime
import hmac
import hashlib
from contextlib import contextmanager
from collections import Iterable
from random import choice
from flask import escape
import string


def generate_user_hash(*args):
    s = ''
    for arg in args:
        s += str(arg)

    return hashlib.sha256().hexdigest()


def generate_captcha(app):
    def rnd_char():
        return chr(random.randint(65, 90))

    # 随机颜色1:
    def rnd_color():
        return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)

    # 随机颜色2:
    def rnd_color2():
        return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rnd_color())

    code = ''

    # 输出文字:
    for t in range(4):
        tmp = rnd_char()
        code += tmp
        draw.text((60 * t + 10, 10), tmp, font=font, fill=rnd_color2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    file_name = str(uuid.uuid4()) + '.png'
    local_path = os.path.join(tempfile.gettempdir(), file_name)

    image.save(local_path, 'png')

    access_key_id = 'LTAIsLk2fj3SuV7y'
    access_key_secret = 'OyAxjkuAFoQqsJ3wTPB0JeRTZiAFkK'
    bucket_name = 'apl-verification-code'
    endpoint = app.config['BUCKET_VCODE_ENDPOINT']

    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    bucket.put_object_from_file(file_name, local_path)
    os.remove(local_path)

    return code, file_name


def generate_verification_code():
    value = random.randint(0, 9999)

    return '%04d' % value


def validate_email(email):
    if re.match(r'^.+@([^.@][^@]+)$', email):
        return True
    return False


def get_iso_8601(expire):
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_sign_policy(key, policy):
    return base64.encodebytes(hmac.new(bytes(key.encode("utf-8")), policy, hashlib.sha1).digest()).strip()


@contextmanager
def safe_session(db):
    try:
        yield
        db.session.commit()
    except:
        db.session.rollback()
        raise
    # finally:
    #     db.session.close()


def merge(obj, dic, ignore=()):
    for key, value in dic.items():
        if isinstance(ignore, Iterable) and key in ignore:
            continue

        if hasattr(obj, key):
            if isinstance(value, str):
                safe_value = str(escape(value))
                setattr(obj, key, safe_value)
            else:
                setattr(obj, key, value)


def check_permission_values(enumeration):
    illegal_values = []
    for name, member in enumeration.__members__.items():
        if member and (member.value & member.value - 1) != 0:
            illegal_values.append((name, member.value))
    if illegal_values:
        errors = ', '.join(
            ["%s -> %s" % (name, value) for (name, value) in illegal_values])
        raise ValueError(
            'Illegal values found in %r: %s' % (enumeration, errors))
    return enumeration


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join([choice(chars) for _ in range(length)])
