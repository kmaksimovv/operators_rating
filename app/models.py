from app import db
from datetime import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(20), index=True)
    queue = db.Column(db.String(20), index=True)
    callerid = db.Column(db.String(20), index=True)
    opinion = db.Column(db.String(1))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return '<Rating operator:{} and opinion: {}>'.format(self.operator, self.opinion)    
