from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField,  DateTimeField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    operator = StringField("Оператор:")
    callerid = StringField("По номеру:")
    start_date = DateField('Начало Даты')
    end_date = DateField('Конец Даты')

class SearchByDateGraph(FlaskForm):
    start_date =  DateTimeLocalField('Начало даты', default=datetime.today, format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end_date =  DateTimeLocalField('Конец даты', default=datetime.today, format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
