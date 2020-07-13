from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    operator = StringField("Оператор:")
    callerid = StringField("По номеру:")
