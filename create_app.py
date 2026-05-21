from flask import Flask
from config import config
from app.extensions import db
from app.route.user import bp as user_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
    app.config['SECRET_KEY'] = config['SECRET_KEY']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_bp)

    return app
