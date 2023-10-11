from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, RadioField, StringField, FieldList, FormField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    include = RadioField('Iekļaut sarakstā', choices=[
                         'Jā', 'Nē'], validators=[DataRequired()])
    teksts = StringField('kaut kāds teksts')


class ReviewMedicationFormList(FlaskForm):
    medications = FieldList(FormField(ReviewMedicationForm), min_entries=1)
    submit = SubmitField('Apstiprināt')
