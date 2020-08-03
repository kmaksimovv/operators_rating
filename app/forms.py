from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms import StringField, SubmitField, DateTimeField, PasswordField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, DataRequired

class SearchForm(FlaskForm):
    operator = StringField("оператор:")
    callerid = StringField("номер:")
    start_date =  DateTimeLocalField('начало даты', format='%Y-%m-%dT%H:%M')
    end_date =  DateTimeLocalField('конец даты', format='%Y-%m-%dT%H:%M')

class SearchByDateGraph(FlaskForm):
    start_date =  DateTimeLocalField('Начало даты', default=datetime.today, format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    end_date =  DateTimeLocalField('Конец даты', default=datetime.today, format='%Y-%m-%dT%H:%M', validators=[InputRequired()])

class LoginForm(FlaskForm):
    login = StringField("логин", validators=[DataRequired()])
    password = PasswordField("пароль", validators=[DataRequired()])
