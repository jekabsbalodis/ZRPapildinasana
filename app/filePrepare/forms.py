from flask_wtf import FlaskForm
from datetime import date
from wtforms import SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    sumbit = SubmitField('Apstiprināt')

# TODO: Izmantot AddedMedication, lai veidotu ciklu cauri pievienojamajiem medikamentiem
class ReviewMedicationForm(FlaskForm):
    sumbit = SubmitField('Apstiprināt')

# class CheckMedicationForm(FlaskForm):
#     include = BooleanField('Iekļaut sarakstā')
#     sumbit = SubmitField('Apstiprināt')
