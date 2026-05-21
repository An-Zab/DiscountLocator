from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.extensions import db
from app.models.user import User



bp = Blueprint('user', __name__)

@bp.route('/test')
def users_list():
    from app.models.user import User
    users = User.query.all()
    print("USERS FOUND:", users)  # выведет в консоль
    print("COUNT:", len(users))
    return render_template('test.html', users=users)