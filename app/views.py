from app import app
from app import db
from app import excel
from flask import render_template, url_for
from .models import Rating
from .forms import *
from sqlalchemy import func
from datetime import date, datetime
from flask import request, redirect
from flask import send_file

@app.route('/results')
def search_results(search):
    ratings = []
    form = SearchForm(request.form)
    
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
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).limit(15).all()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    return render_template('graph.html', labels=labels, values=values)

@app.route('/graph-today')
def graph_today():
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).limit(15).all()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    return render_template('graph.html', labels=labels, values=values)

@app.route('/graph-yesterday')
def graph_yesterday():
    ratings = db.session.query(Rating).order_by(db.asc(Rating.created_at)).limit(15).all()
    labels = []
    values = []
    
    for r in ratings:
        labels.append(r.format_created_at())
        values.append(r.value)
    return render_template('graph.html', labels=labels, values=values)

@app.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_a_table(db.session, Rating, "xlsx", file_name="sheet")

@app.route('/custom_export_report')
def custom_export_report(form):
    operator = request.form.get('operator').strip()
    callerid = request.form.get('callerid').strip()
    start_date = request.form.get('start_date').strip()
    end_date = request.form.get('end_date').strip()
    column_names = ['id', 'operator', 'queue', 'callerid', 'value', 'created_at']

    if operator and callerid and start_date and end_date:
        query_sets = db.session.query(Rating).filter(Rating.operator == operator, Rating.callerid == callerid).filter(Rating.created_at.between(start_date, end_date)).all()
        return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name=f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    elif operator and callerid:
        query_sets = db.session.query(Rating).filter_by(operator=operator, callerid=callerid).all()
        return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name=f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    elif start_date and end_date:
        query_sets = db.session.query(Rating).filter(Rating.created_at.between(start_date, end_date)).all()
        return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name=f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    elif operator:
        query_sets = db.session.query(Rating).filter_by(operator=operator).all()
        return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name=f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    elif callerid:
        query_sets = db.session.query(Rating).filter_by(callerid=callerid).all()
        return excel.make_response_from_query_sets(query_sets, column_names,"xlsx", file_name=f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    else:
        return render_template("report.html", form=form)

@app.route("/custom_export", methods=['GET', 'POST'])
def custom_export():
    form = SearchForm()
    
    if request.method == 'POST':
        return custom_export_report(form)
    
    return render_template("report.html", form=form)

@app.route("/rating-by-operator", methods=['GET'])
def rating_by_operator():
    operators = [r[0] for r in db.session.query(Rating.operator).distinct().all()]
    rating_by_operators = []
    
    for index, operator in enumerate(operators):
        rat = Rating()
        rat.id = index
        rat.operator = operator 
        rat.labels = [r[0].strftime("%m-%d %H:%M") for r in db.session.query(Rating).order_by(db.asc(Rating.created_at)).filter_by(operator=operator).limit(10).values('created_at')]
        rat.values = [r[0] for r in db.session.query(Rating).order_by(db.asc(Rating.created_at)).filter_by(operator=operator).limit(10).values('value')]
        rating_by_operators.append(rat)
    
    return render_template('rating_by_operator.html', ratings=rating_by_operators)

@app.route('/get_xslx_for_data')
def get_xslx_for_data():
    import xlsxwriter
    from xlsxwriter.workbook import Workbook
    from io import BytesIO
    name_file = f"report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.xlsx"
    workbook = xlsxwriter.Workbook(name_file)
    worksheet = workbook.add_worksheet()
    ratings = db.session.query(Rating).all()
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
    
    return send_file('../' + name_file, as_attachment=True, cache_timeout=0)


