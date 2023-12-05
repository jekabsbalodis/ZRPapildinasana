from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField
from wtforms.validators import DataRequired


class AtcSearchForm(FlaskForm):
    atcCode = SearchField('Meklēt pēc ATĶ koda', validators=[DataRequired()])
    searchAtcCode = SubmitField('Meklēt')
