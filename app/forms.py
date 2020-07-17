from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    operator = StringField("Оператор:")
    callerid = StringField("По номеру:")
    start_date = DateField('Начало Даты')
    end_date = DateField('Конец Даты')

