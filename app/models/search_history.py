from app.extensions import db

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String(100), nullable=False)
    searched_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())