from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AtcSearchForm(FlaskForm):
    atcCode = SearchField('Meklēt pēc ATĶ koda', validators=[DataRequired()])
    searchAtcCode = SubmitField('Meklēt')


class NameSearchForm(FlaskForm):
    name = SearchField('Meklēt pēc aktīvās vielas nosaukuma', validators=[DataRequired()])
    searchName = SubmitField('Meklēt')


class RegSearchForm(FlaskForm):
    regNumber = SearchField('Meklēt pēc reģistrācijas numura', validators=[DataRequired()])
    searchRegNumber = SubmitField('Meklēt')
