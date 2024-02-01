'''ZRApp configuration variables'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''ZRApp base configuration'''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS').lower() in [
        'true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ZRAPP_MAIL_SUBJECT_PREFIX = '[ZRApp]'
    ZRAPP_MAIL_SENDER = 'ZRApp Admin <zrapp@inbox.lv>'
    ZRAPP_ADMIN = os.environ.get('ZRAPP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    DATA_GOV_LV_RESOURCE_ID = os.environ.get('DATA_GOV_LV_RESOURCE_ID')
    DATA_GOV_LV_API_KEY = os.environ.get('DATA_GOV_LV_API_KEY')
    ZVA_USER_NAME = os.environ.get('ZVA_USER_NAME')
    ZVA_PASSWORD = os.environ.get('ZVA_PASSWORD')
    ZVA_FTP_ADDRESS = os.environ.get('ZVA_FTP_ADDRESS')
    ZVA_FTP_PORT = os.environ.get('ZVA_FTP_PORT')
    # BOOTSTRAP_BOOTSWATCH_THEME = 'cosmo'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    '''ZRApp development configuration'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    '''ZRApp testing configuration'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    '''ZRApp production configuration'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrator
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.ZRAPP_MAIL_SENDER,
            toaddrs=[cls.ZRAPP_ADMIN],
            subject=cls.ZRAPP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class PythonAnywhereConfig(ProductionConfig):
    '''ZRApp configuration for PythonAnywhere'''
    SSL_REDIRECT = True

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):
    '''ZRapp configuration for Docker deployment'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/data.sqlite')

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'pythonanywhere': PythonAnywhereConfig,
    'docker': DockerConfig,

    'default': DevelopmentConfig
}
