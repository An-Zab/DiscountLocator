from app.extensions import db


class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    interval_hours = db.Column(db.Integer, default=24)
    last_checked = db.Column(db.TIMESTAMP, nullable=True)
    active = db.Column(db.Boolean, default=True)
