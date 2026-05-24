from flask import Flask, render_template
from app.config import config
from app.extensions import db, login_manager
from app.route.user import bp as user_bp
from app.models.user import User
from app.route.search import bp as search_bp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
    app.config['SECRET_KEY'] = config['SECRET_KEY']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    app.register_blueprint(search_bp)

    return app