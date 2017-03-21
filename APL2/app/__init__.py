from flask import Flask, config, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
# from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.fixers import ProxyFix
from flask_loginmanager import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from pymysql.err import IntegrityError
import logging


db = SQLAlchemy()
mail = Mail()
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
    mail.init_app(app)
    # DebugToolbarExtension(app)
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
    app.register_blueprint(admin, url_prefix='/sudo')

    from .api.v_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v_1_0')

    if not app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='apl_internal.log',
                            filemode='w')

    # @app.errorhandler(400)
    # def something_happened(e):
    #
    #     print("something_happened :", e)
    #
    #     return 'APL Internal Error: %s' % e
    #
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
    #         response = jsonify({'status': 1, 'message': 'not found'})
    #         response.status_code = 404
    #
    #         print('page_not_found mobile:', e)
    #
    #         return response
    #
    #     print('page_not_found web:', e)
    #
    #     return "Page Not Found Globally: %s" % e
    #
    # @app.errorhandler(500)
    # @app.errorhandler(Exception)
    # def server_error(e):
    #     if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
    #         response = jsonify({'status': 1, 'message': 'server error'})
    #         response.status_code = 500
    #         print("APL Server Error mobile：", e)
    #         return response
    #
    #     print("APL Server Error web：%s" % e)
    #     return "APL Server Error."

    # TODO 处理email重复的问题
    @app.errorhandler(IntegrityError)
    def duplicat_email():
        print('该Email以存在')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
        print('session remove.')

    return app

