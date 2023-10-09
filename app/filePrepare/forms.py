from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, BooleanField, StringField, FieldList, FormField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    include = BooleanField('Iekļaut sarakstā')
    teksts = StringField('kaut kāds teksts')
    submit = SubmitField('Apstiprināt')


class ReviewMedicationFormList(FlaskForm):
    medications = FieldList(FormField(ReviewMedicationForm), min_entries=1)
