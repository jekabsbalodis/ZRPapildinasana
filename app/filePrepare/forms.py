from datetime import date
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length


class DownloadForm(FlaskForm):
    dateFrom = DateField('Pēdējās datu atjaunošanas datums',
                         default=date.today() - timedelta(days=1), format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    prohibitedOUTCompetition = SelectField(
        'Vai medikaments ir aizliegts ārpus sacensībām?', choices=['Jā', 'Nē', 'Jā*', 'Ar nosacījumu'], default='Nē')
    prohibitedINCompetition = SelectField(
        'Vai medikaments ir aizliegts sacensību laikā?', choices=['Jā', 'Nē', 'Jā*', 'Ar nosacījumu'], default='Nē')
    prohibitedClass = StringField(
        'Kurai Aizliegto vielu un metožu saraksta klasei medikaments pieder?', validators=[Length(max=10)])
    notesLV = TextAreaField('Piezīmes par medikamenta lietošanu')
    notesEN = TextAreaField('Norādi šo informāciju angliski')
    sportsINCompetitionLV = TextAreaField(
        'Ja medikaments aizliegts tikai noteiktos sporta veidos sacensību laikā, norādi šos sporta veidus')
    sportsINCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    sportsOUTCompetitionLV = TextAreaField(
        'Ja medikaments aizliegts tikai noteiktos sporta veidos ārpus sacensībām, norādi šos sporta veidus')
    sportsOUTCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    include = SubmitField('Apstiprināt')
    notInclude = SubmitField('Neiekļaut nododamajos datos')


class UploadZVAFrom(FlaskForm):
    userName = StringField('Lietotāja vārds', validators=[DataRequired()])
    passWord = PasswordField('Parole', validators=[DataRequired()])
    ftpAddress = StringField('Servera adrese', validators=[DataRequired()])
    ftpPort = IntegerField('Servera ports', validators=[DataRequired()])
    submitZVA = SubmitField('Apstiprināt')


class UploadDataGovLVForm(FlaskForm):
    resourceID = StringField('Resursa ID numurs', validators=[DataRequired()])
    apiKey = PasswordField('api atslēga', validators=[DataRequired()])
    submitDataGovLV = SubmitField('Apstiprināt')
