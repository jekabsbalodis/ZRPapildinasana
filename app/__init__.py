from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap5()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Lai apmeklētu šo lapu, lūdzu pieslēdzieties sistēmai"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)    

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .reg import reg as reg_blueprint
    app.register_blueprint(reg_blueprint, url_prefix='/reg')

    from .filePrepare import filePrepare as filePrepare_blueprint
    app.register_blueprint(filePrepare_blueprint, url_prefix='/filePrepare')

    return app
