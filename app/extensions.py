from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import current_app



#DATABASE
db = SQLAlchemy()



#LOGIN MANAGER
login_manager = LoginManager()
login_manager.login_view = 'user.login'


