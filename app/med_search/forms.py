'''Forms for searching for mediciation'''
from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField
from wtforms.validators import DataRequired


class AtcSearchForm(FlaskForm):
    '''Form to provide ATC code for search'''
    atcCode = SearchField('Meklēt pēc ATĶ koda', validators=[DataRequired()])
    searchAtcCode = SubmitField('Meklēt')


class NameSearchForm(FlaskForm):
    '''Form to provide active substance name for search'''
    name = SearchField('Meklēt pēc aktīvās vielas nosaukuma', validators=[DataRequired()])
    searchName = SubmitField('Meklēt')


class RegSearchForm(FlaskForm):
    '''Form to provide registration number for search'''
    regNumber = SearchField('Meklēt pēc reģistrācijas numura', validators=[DataRequired()])
    searchRegNumber = SubmitField('Meklēt')
