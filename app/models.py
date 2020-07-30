from app import db
from datetime import datetime
from sqlalchemy import desc
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin

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

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.login)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)
