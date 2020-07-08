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
    #data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    #data = [{'data': [['2013-04-01 00:00:00 UTC', 52.9], ['2013-05-01 00:00:00 UTC', 50.7]], 'operator': 'Chrome'},
            # {'data': [['2013-04-01 00:00:00 UTC', 27.7], ['2013-05-01 00:00:00 UTC', 25.9]], 'operator': 'Firefox'}]
    
            
    data = dict(db.session.query(Rating.operator, Rating.value).all())
    # data = dict(db.session.query(Rating.operator, Rating.created_at).all())
    
    return render_template('graph.html', data=data)
