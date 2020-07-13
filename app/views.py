from app import app
from app import db
from app import excel
from flask import render_template, url_for
from .models import Rating
from .forms import SearchForm
from sqlalchemy import func
from datetime import date
from flask import request, redirect

@app.route('/results')
def search_results(search):
    ratings = []
    form = SearchForm(request.form)

    if list(search.data.keys())[0] == 'operato':
        search_string = search.data['operator']
        qry = db.session.query(Rating).filter(Rating.operator == search_string)
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)
    elif list(search.data.keys())[1] == 'callerid':
        search_string = search.data['callerid']
        qry = db.session.query(Rating).filter(Rating.callerid == search_string)
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)
    else:
        return redirect(url_for('index'))
        

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    
    if request.method == 'POST':
        return search_results(form)
    
    ratings = db.session.query(Rating).order_by(db.desc(Rating.id)).all()
    return render_template('index.html', ratings=ratings, form=form)

@app.route('/graph')
def graph_all():
    data = []
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).all()
    
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)

@app.route('/graph-today')
def graph_today():
    data = []
    ratings = db.session.query(Rating).filter(func.date(Rating.created_at) == date.today()).all()
    
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)

@app.route('/graph-yesterday')
def graph_yesterday():
    data = []
    ratings = db.session.query(Rating).filter(func.date(Rating.created_at) == date.today()).all()
    
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)


@app.route("/export", methods=['GET'])
def doexport():
    excel.init_excel(app)
    return excel.make_response_from_a_table(db.session, Rating, "xls", file_name='data') 
