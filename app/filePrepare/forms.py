from datetime import date
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    prohibitedOUTCompetition = BooleanField(
        'Vai medikaments ir aizliegts ārpus sacensībām?')
    prohibitedINCompetition = BooleanField(
        'Vai medikaments ir aizliegts sacensību laikā?')
    prohibitedClass = StringField('Kurai Aizliegto vielu un metožu saraksta klasei medikaments pieder?', validators=[Length(max=10)])
    notesLV = TextAreaField('Piezīmes par medikamenta lietošanu')
    notesEN = TextAreaField('Norādi šo informāciju angliski')
    sportsINCompetitionLV = TextAreaField('Ja medikaments aizliegts tikai noteiktos sporta veidos sacensību laikā, norādi šos sporta veidus')
    sportsINCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    sportsOUTCompetitionLV = TextAreaField('Ja medikaments aizliegts tikai noteiktos sporta veidos ārpus sacensībām, norādi šos sporta veidus')
    sportsOUTCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    include = SubmitField('Apstiprināt')
    notInclude = SubmitField('Neiekļaut nododamajos datos')
