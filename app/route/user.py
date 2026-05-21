from flask import Blueprint, render_template
from app.models import User

bp = Blueprint('user', __name__)


@bp.route('/test')
def users_list():
    users = User.query.all()
    return render_template('test.html', users=users)
