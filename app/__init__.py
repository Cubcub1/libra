from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
# LoginManager对象的session_protection属性可以设为None 'basic' 'strong' 已提供不同的安全等级防止用户回话遭篡改，
# 设为'strong'，flask-login会记录客户端ip地址和浏览器的用户代理信息，如果有移动就登出用户
login_manager.session_protection = 'strong'
# login_view属性设置登录页面的端点
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
