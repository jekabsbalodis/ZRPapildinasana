from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AtcSearchForm(FlaskForm):
    atcCode = SearchField('Meklēt pēc ATĶ koda', validators=[DataRequired()])
    searchAtcCode = SubmitField('Meklēt')
