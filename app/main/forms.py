from flask_wtf import FlaskForm
from datetime import date
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Iesniegt')
