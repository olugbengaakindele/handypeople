# app/init
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

mail = Mail()
sr = URLSafeTimedSerializer(os.environ['e_data_password'])
login_manager = LoginManager()
login_manager.login_view = "auth.do_the_login"
login_manager.session_protection= "strong"
bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app(env):

    myapp = Flask(__name__)
    config_file = os.path.join(os.getcwd(),'config',f'{env}.py')
    myapp.config.from_pyfile(config_file)

    db.init_app(myapp)

    from app.auth import auth
    myapp.register_blueprint(auth)

    from app.catlog import cat
    myapp.register_blueprint(cat)

    login_manager.init_app(myapp)
    bcrypt.init_app(myapp)
    mail.init_app(myapp)
   
    return myapp



