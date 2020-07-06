from app import app
from app import db
from flask import render_template
from .models import Rating

@app.route('/')
def index():
    ratings = db.session.query(Rating).order_by(db.desc(Rating.id)).all()
    return render_template('index.html', ratings=ratings)
