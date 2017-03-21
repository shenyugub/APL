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

