#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/21 上午11:56
# @Author  : Rain
# @Desc    :
# @File    : __init__.py.py


from flask import render_template, redirect, url_for, current_app, request, flash, make_response, jsonify, session
from app.utils.utils import generate_captcha, generate_verification_code, validate_email
from app import user_manager, db, csrf
from app.models import Startup, File
from app.utils.mail import send
from app.utils.utils import safe_session
from flask import Blueprint


main = Blueprint('main', __name__)


@main.route('/send_forget_password_email/')
def send_forget_password_email():
    email = request.args.get('email')
    if validate_email(email):
        code = generate_verification_code()
        session['email_code'] = code
        session['email'] = email
        result = send(email, 'APL 密码找回', render_template('mail_forget_password.html', code=code), render_template('mail_forget_password.txt', code=code))
        if result:
            return "发送成功"
        else:
            return "发送失败"
    else:
        return "非法邮件地址"


@main.route('/v_code')
def prepare_v_code():
    code, path = generate_captcha(current_app)

    session['vcode'] = code

    return 'https://apl-verification-code.oss-cn-shanghai.aliyuncs.com/' + path


@user_manager.user_loader
def user_loader(uid):
    uid = str(uid)
    if uid is None:
        return None

    try:
        return Startup.query.get(uid)

    except TypeError:
        return None
    except ValueError:
        return None


@user_manager.failure_handler
def failure_handler():
    # return 'You should login first: %s' % request.blueprint

    print('please login first')
    return redirect(url_for('main.index'))


@user_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, user_manager.expires, user_manager.salt)


@main.route('/test_mail')
def test_email():
    from app.utils.sms import send

    # result = send('chenqing@apluslabs.com', 'test mail', render_template('mail_forget_password.html', url='www.baidu.com'), render_template('mail_reset_password.txt', url='www.baidu.com'))
    result = send('18120192260', '6789')
    if result:
        return 'ok'
    return 'fail'


@main.route('/test_bucket')
def test_bucket():
    from app.utils.sts import request_sts_token
    request_sts_token('rain')

    return 'ok'


@csrf.exempt
@main.route('/after_upload', methods=['GET', 'POST'])
def after_upload():
    # 调试这个接口时，关闭supervisor，像在本地一样自己远程启动云服务器，然后看控制台输出，要切换到调试模式

    data = request.form.to_dict()

    bucket = data.get('bucket', '')
    obj = data.get('object', '')
    etag = data.get('etag', '')
    size = data.get('size', '')
    mime_type = data.get('mimeType', '')
    uid = data.get('uid', '')  # 注意，自定义参数在这里访问的时候没有 x:
    phase_id = data.get('phase_id', '')
    filename = data.get('filename', '')

    f = File()
    f.owner_id = uid
    f.local_name = filename
    f.server_name = obj

    with safe_session(db):
        db.session.add(f)

    result = {"bucket": bucket, "obj": obj, "etag": etag, "size": size, "mime_type": mime_type, "uid": uid, "phase_id": phase_id, "filename": filename}

    result = jsonify(result)

    resp = make_response(result, 200)
    resp.headers['Content-Length'] = str(len(resp.data))

    return resp


@main.route('/download_url', methods=['GET'])
@user_manager.login_required()  # 后添加的，如果不能正常下载请检查这里
def get_url():
    from app.utils.sts import get_file_url
    url = get_file_url('demo.jpg', 'apple.jpg')
    return url

