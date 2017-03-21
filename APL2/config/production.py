from .config import Config


class Production(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = '&*y32hkds8ih^%3hkjhsd8%8098432k78'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://server:2Uz3e7yk-mwwdhio^s2y75dj@rm-2ze9uiue6mo09e0m9.mysql.rds.aliyuncs.com/apl'
    BUCKET_VCODE_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
    STS_DURATION_SECONDS = 1800
