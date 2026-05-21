from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telegram_id = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
