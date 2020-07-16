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
    print(search.data)
    
    if search.data['operator'] and search.data['callerid'] and search.data['start_date'] and search.data['end_date']:
        search_string_operator = search.data['operator'].strip()
        search_string_callerid = search.data['callerid'].strip()
        search_start_date = search.data['start_date']
        search_end_date = search.data['end_date']
        qry = db.session.query(Rating).filter(Rating.operator == search_string_operator, Rating.callerid == search_string_callerid).filter(Rating.created_at.between(search_start_date, search_end_date))
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)
    elif search.data['operator'] and search.data['start_date'] and search.data['end_date']:
        search_string_operator = search.data['operator'].strip()
        search_start_date = search.data['start_date']
        search_end_date = search.data['end_date']
        qry = db.session.query(Rating).filter(Rating.operator == search_string_operator, Rating.created_at.between(search_start_date, search_end_date))
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)
    elif search.data['callerid'] and search.data['start_date'] and search.data['end_date']:
        search_string = search.data['callerid'].strip()
        search_start_date = search.data['start_date']
        search_end_date = search.data['end_date']
        qry = db.session.query(Rating).filter(Rating.callerid == search_string_callerid, Rating.created_at.between(search_start_date, search_end_date))
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)        
    elif search.data['operator'] and search.data['callerid']:
        search_string_operator = search.data['operator'].strip()
        search_string_callerid = search.data['callerid'].strip()
        qry = db.session.query(Rating).filter(Rating.operator == search_string_operator, Rating.callerid == search_string_callerid)
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)    
    elif search.data['operator']:
        search_string = search.data['operator'].strip()
        qry = db.session.query(Rating).filter(Rating.operator == search_string)
        ratings = qry.all()
        return render_template('index.html', ratings=ratings, form=form)
    elif search.data['callerid']:
        search_string = search.data['callerid'].strip()
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
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).limit(10).all()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    bar_labels=labels
    bar_values=values
    return render_template('graph.html', labels=bar_labels, values=bar_values)

@app.route('/graph-today')
def graph_today():
    data = []
    ratings = db.session.query(Rating).filter(func.date(Rating.created_at) == date.today()).limit(10).all()
    
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)

@app.route('/graph-yesterday')
def graph_yesterday():
    data = []
    ratings = db.session.query(Rating).filter(func.date(Rating.created_at) == date.today()).limit(10).all()
    
    for r in ratings:
        data.append([r.format_created_at(), r.value])
    
    return render_template('graph.html', data=data)


@app.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_a_table(db.session, Rating, "xlsx", file_name="sheet")

@app.route("/custom_export", methods=['GET'])
def docustomexport():
    query_sets = db.session.query(Rating).all()
    column_names = ['id', 'operator', 'queue', 'callerid', 'value', 'created_at']
    return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name="sheet")    


@app.route("/rating-by-operator", methods=['GET'])
def rating_by_operator():
    operators = [r[0] for r in db.session.query(Rating.operator).distinct().all()]
    rating_by_operators = []
    
    for index, operator in enumerate(operators):
        rat = Rating()
        rat.id = index
        rat.operator = operator 
        rat.labels = [r[0].strftime("%m-%d %H:%M") for r in db.session.query(Rating).filter_by(operator=operator).values('created_at')]
        rat.values = [r[0] for r in db.session.query(Rating).filter_by(operator=operator).values('value')]
        rating_by_operators.append(rat)
    
    return render_template('rating_by_operator.html', ratings=rating_by_operators)

