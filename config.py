import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ļoti grūta parole'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'mail.inbox.lv')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = ('MAIL_USERNAME')
    MAIL_PASSWORD = ('MAIL_PASSWORD')
    ZRAPP_MAIL_SUBJECT_PREFIX = '[ZRApp]'
    ZRAPP_MAIL_SENDER = 'ZRApp Admin <myhood@inbox.lv>'
    ZRAPP_ADMIN = os.environ.get('ZRAPP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_REG_DOMAINS = ['inbox.lv']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
