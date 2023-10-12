from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, BooleanField, StringField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    prohibitedINCompetition = BooleanField('Vai medikaments ir aizliegts sportā?')
    teksts = StringField('kaut kāds teksts')
    submit = SubmitField('Apstiprināt')
