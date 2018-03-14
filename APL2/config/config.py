class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024 #上传文件的尺寸
    SQLALCHEMY_POOL_TIMEOUT = 900 #指定数据库连接池的超时时间
    SQLALCHEMY_POOL_RECYCLE = 900 #自动回收连接的秒数
    SQLALCHEMY_POOL_SIZE = 300 #数据库连接池的大小
    SQLALCHEMY_MAX_OVERFLOW = 50 #控制在连接池达到最大值后可以创建的连接数


def init_app(app):
    pass
