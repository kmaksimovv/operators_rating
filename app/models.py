from app import db
from datetime import datetime
from sqlalchemy import desc

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(20), index=True)
    queue = db.Column(db.String(20), index=True)
    callerid = db.Column(db.String(20), index=True)
    value = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now)
    
    def __repr__(self):
        return '<Rating operator:{}>'.format(self.operator)
    
    def format_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def list_all_pagination(self, page, LISTINGS_PER_PAGE):
        return Rating.query.order_by(desc(Rating.id)).paginate(page, LISTINGS_PER_PAGE, False)
