from app import app
from app import db
from flask import render_template, url_for
from .models import Rating

@app.route('/')
def index():
    ratings = db.session.query(Rating).order_by(db.desc(Rating.id)).all()
    return render_template('index.html', ratings=ratings)

@app.route('/chart')
def first_graph():
    data = []
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).all()
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)
