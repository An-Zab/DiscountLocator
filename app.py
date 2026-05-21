from flask import Flask, render_template
import config
from app.extensions import db
from app.route.user import bp as user_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.config['DATABASE_URI']
app.config['SECRET_KEY'] = config.config['SECRET_KEY']

db.init_app(app)

app.register_blueprint(user_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)