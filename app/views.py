import os
from app import app
from app import db
from flask import render_template, url_for
from .models import Rating
from .forms import *
from sqlalchemy import func
from datetime import date, datetime, timedelta
from flask import request, redirect
from flask import send_file
from xlsxwriter.workbook import Workbook
from flask import after_this_request
from sqlalchemy import cast, DATE

@app.route('/results')
def search_results(search):
    ratings = []
    form = SearchForm(request.form)
    
    operator = str(request.form.get('operator')).strip()
    callerid = request.form.get('callerid').strip()
    start_date = request.form.get('start_date').strip()
    end_date = request.form.get('end_date').strip()
    
    if operator and callerid and start_date and end_date:
        query_sets = db.session.query(Rating).filter(Rating.operator == operator, Rating.callerid == callerid).filter(Rating.created_at.between(start_date, end_date)).all()

        return render_template('index.html', ratings=query_sets, form=form)
    elif operator and callerid:
        query_sets = db.session.query(Rating).filter_by(operator=operator, callerid=callerid).all()

        return render_template('index.html', ratings=query_sets, form=form)
    elif operator and start_date and end_date:
        query_sets = db.session.query(Rating).filter_by(operator=operator).filter(Rating.created_at.between(start_date, end_date)).all()

        return render_template('index.html', ratings=query_sets, form=form)
    elif callerid and start_date and end_date:
        query_sets = db.session.query(Rating).filter_by(callerid=callerid).filter(Rating.created_at.between(start_date, end_date)).all()
        
        return render_template('index.html', ratings=query_sets, form=form)
    elif operator:
        query_sets = db.session.query(Rating).filter_by(operator=operator).all()
        
        return render_template('index.html', ratings=query_sets, form=form)
    elif callerid:
        query_sets = db.session.query(Rating).filter_by(callerid=callerid).all()
        
        return render_template('index.html', ratings=query_sets, form=form)
    else:
        return redirect(url_for('index'))
        

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    
    if request.method == 'POST':
        return search_results(form)
    
    ratings = db.session.query(Rating).order_by(db.desc(Rating.id)).all()
    return render_template('index.html', ratings=ratings, form=form)

@app.route('/graph-today')
def graph_today(count=15):
    ratings = db.session.query(Rating).filter(cast(Rating.created_at, DATE) == date.today()).order_by(db.desc(Rating.id)).limit(count).all()
    ratings.reverse()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    return render_template('graph.html', labels=labels, values=values)

@app.route('/graph-yesterday')
def graph_yesterday(count=15):
    yesterday = date.today() - timedelta(days=1)
    ratings = db.session.query(Rating).filter(Rating.created_at.like("%{}%".format(yesterday))).all()
    ratings.reverse()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    return render_template('graph.html', labels=labels, values=values)



@app.route("/rating-by-operator", methods=['GET'])
def rating_by_operator():
    operators = [r[0] for r in db.session.query(Rating.operator).distinct().all()]
    rating_by_operators = []
    
    for index, operator in enumerate(operators):
        rat = Rating()
        rat.id = index
        rat.operator = operator 
        rat.labels = [r[0].strftime("%m-%d %H:%M:%S") for r in db.session.query(Rating).order_by(db.desc(Rating.id)).filter_by(operator=operator).limit(10).values('created_at')]
        rat.values = [r[0] for r in db.session.query(Rating).order_by(db.desc(Rating.id)).filter_by(operator=operator).limit(10).values('value')]
        rating_by_operators.append(rat)
    
    for r in rating_by_operators:
        r.labels.reverse()
        r.values.reverse()

    return render_template('rating_by_operator.html', ratings=rating_by_operators)

@app.route('/get_xslx_for_data')
def get_xslx_for_data(ratings):

    
    name_file = f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.xlsx"
    workbook = Workbook(name_file)
    worksheet = workbook.add_worksheet("Оценка")
    worksheet.write(0,0, "ид")
    worksheet.write(0,1, "оператор")
    worksheet.write(0,2, "очередь")
    worksheet.write(0,3, "аон")
    worksheet.write(0,4, "оценка")
    worksheet.write(0,5, "дата")
    
    row = 1
    col = 0
    for rating in ratings:
        worksheet.write(row, col, rating.id)
        worksheet.write(row, col + 1, rating.operator)
        worksheet.write(row, col + 2, rating.queue)
        worksheet.write(row, col + 3, rating.callerid)
        worksheet.write(row, col + 4, rating.value)
        worksheet.write(row, col + 5, rating.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        row += 1
        
    
    workbook.close()

    @after_this_request
    def remove_file(response):
        try:
            os.remove(name_file)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    
    return send_file('../' + name_file, as_attachment=True, cache_timeout=0)


@app.route('/custom_export_report')
def custom_export_report(form):
    operator = request.form.get('operator').strip()
    callerid = request.form.get('callerid').strip()
    start_date = request.form.get('start_date').strip()
    end_date = request.form.get('end_date').strip()
    
    if operator and callerid and start_date and end_date:
        query_sets = db.session.query(Rating).filter(Rating.operator == operator, Rating.callerid == callerid).filter(Rating.created_at.between(start_date, end_date)).all()

        return get_xslx_for_data(query_sets)
    elif operator and callerid:
        query_sets = db.session.query(Rating).filter_by(operator=operator, callerid=callerid).all()

        return get_xslx_for_data(query_sets)
    elif operator and start_date and end_date:
        query_sets = db.session.query(Rating).filter_by(operator=operator).filter(Rating.created_at.between(start_date, end_date)).all()

        return get_xslx_for_data(query_sets)
    elif callerid and start_date and end_date:
        query_sets = db.session.query(Rating).filter_by(callerid=callerid).filter(Rating.created_at.between(start_date, end_date)).all()

        return get_xslx_for_data(query_sets)
    elif operator:
        query_sets = db.session.query(Rating).filter_by(operator=operator).all()

        return get_xslx_for_data(query_sets)
    elif callerid:
        query_sets = db.session.query(Rating).filter_by(callerid=callerid).all()

        return get_xslx_for_data(query_sets)
    else:
        return render_template("report.html", form=form)
    
@app.route("/custom_export", methods=['GET', 'POST'])
def custom_export():
    form = SearchForm()
    
    if request.method == 'POST':
        return custom_export_report(form)
    
    return render_template("report.html", form=form)
