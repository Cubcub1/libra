import os


class Config:
    SECRET_KEY = "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    LIBRA_MAIL_SUBJECT_PREFIX = '[Libra]'
    LIBRA_MAIL_SENDER = 'Libra Admin <lx_0308@163.com>'
    # 接受邮件的项目admin账号
    LIBRA_ADMIN = os.environ.get('LIBRA_ADMIN')
    LIBRA_POSTS_PER_PAGE = 5
    LIBRA_FOLLOWERS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCT_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductConfig,
    'default': DevelopmentConfig
}
