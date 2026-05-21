from app.extensions import db


class SearchResult(db.Model):
    __tablename__ = 'search_result'

    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('search_history.id'), nullable=False)
    product = db.Column(db.String(100))
    shop_name = db.Column(db.String(100))
    product_price = db.Column(db.String(50))
    shop_phones = db.Column(db.Text)
    shop_social_media = db.Column(db.Text)
    placement = db.Column(db.String(100))
    url = db.Column(db.String(150))
    offertimestamp = db.Column(db.BigInteger)
