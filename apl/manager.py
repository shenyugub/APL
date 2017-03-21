#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 上午10:36
# @Author  : Rain
# @Desc    : 程序启动类：python manager runserver
# @File    : manager.py


import os
from flask_script import Manager, Server
from app import init_app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import MigrateCommand
from app.utils.utils import generate_password


instance = init_app(os.getenv('config', 'development'))
manager = Manager(instance)
manager.add_command("runserver", Server(host="0.0.0.0"))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    engine = create_engine(instance.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    if not database_exists(engine.url):
        create_database(engine.url)


@manager.command
def gen_secret():
    print(generate_password())


if __name__ == '__main__':
    manager.run()

