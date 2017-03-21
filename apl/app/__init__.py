#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午9:54
# @Author  : Rain
# @Desc    : 程序主类
# @File    : __init__.py

from flask import Flask, config, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
from werkzeug.contrib.fixers import ProxyFix
from flask_loginmanager import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import logging


db = SQLAlchemy()
mail = Mail()
session = Session()
admin_manager = LoginManager(role='admin')
user_manager = LoginManager(role='user')
csrf = CSRFProtect()


def init_app(profile):

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if profile == 'development':
        from config.development import Development
        app.config.from_object(Development)
    else:
        from config.production import Production
        app.config.from_object(Production)

    config.init_app(app)
    db.init_app(app)
    session.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    admin_manager.init_app(app)
    user_manager.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .startup import startup
    app.register_blueprint(startup, url_prefix='/startup')

    from .investor import investor
    app.register_blueprint(investor, url_prefix='/investor')

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    if not app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='apl_internal.log',
                            filemode='w')
    else:
        admin_manager.expires = app.config['ADMIN_SESSION_EXPIRE']
        user_manager.expires = app.config['STARTUP_SESSION_EXPIRE']

    # 移除数据库连接，可能不需要，所以先注释掉
    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db.session.remove()
    #     print('session remove.')

    return app
