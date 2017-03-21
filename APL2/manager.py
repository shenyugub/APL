import os
from flask_script import Manager, Server
from app import init_app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import MigrateCommand
from os import path

instance = init_app(os.getenv('config', 'development'))
manager = Manager(instance)
manager.add_command("runserver", Server(host="0.0.0.0"))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    engine = create_engine(instance.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    if not database_exists(engine.url):
        create_database(engine.url)


if __name__ == '__main__':

    # if instance.config['DEBUG']:
    #     extra_dirs = ['./app/templates', ]
    #     extra_files = extra_dirs[:]
    #     for extra_dir in extra_dirs:
    #         for dirname, dirs, files in os.walk(extra_dir):
    #             for filename in files:
    #                 filename = path.join(dirname, filename)
    #                 if path.isfile(filename):
    #                     extra_files.append(filename)
    #
    #     instance.run(extra_files=extra_files)
    # else:
        manager.run()

    # instance.run()
