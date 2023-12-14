from datetime import datetime
import requests
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length



class DownloadForm(FlaskForm):
    # url = 'https://data.gov.lv/dati/lv/api/3/action/package_show?id=medikamenti-kas-satur-dopinga-vielas'
    # data = requests.get(url).json()
    # lastUpdate = data.get('result').get('resources')[0].get('last_modified')[:10]
    # lastUpdateFormatted = datetime.strptime(lastUpdate, '%Y-%m-%d').date()
    with open('.lastUpdate', encoding='utf-8') as f:
        lastUpdate = f.read()
    lastUpdateFormatted = datetime.strptime(lastUpdate, '%Y-%m-%d').date()
    dateFrom = DateField('No kura datuma pārskatīt medikamentus?',
                         default=lastUpdateFormatted,
                         format='%Y-%m-%d',
                         validators=[DataRequired()])
    #  render_kw={'oninvalid': 'this.setCustomValidity("Ievadi datumu")'})
    #  Atribūts formas laukam, lai nomainītu attēlojamo tekstu,
    #  ja tiek mēģināts iesniegt tukšu lauku
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
    include = SubmitField('Iekļaut')
    bulkInclude = SubmitField('Iekļaut visus līdzīgus medikamentus')
    notInclude = SubmitField('Neiekļaut nododamajos datos')


class UploadZVAForm(FlaskForm):
    userName = StringField('Lietotāja vārds', validators=[DataRequired()])
    passWord = PasswordField('Parole', validators=[DataRequired()])
    ftpAddress = StringField('Servera adrese', validators=[DataRequired()])
    ftpPort = IntegerField('Servera ports', validators=[DataRequired()])
    submitZVA = SubmitField('Apstiprināt')


class UploadDataGovLVForm(FlaskForm):
    resourceID = StringField('Resursa ID numurs', validators=[DataRequired()])
    apiKey = PasswordField('api atslēga', validators=[DataRequired()])
    submitDataGovLV = SubmitField('Apstiprināt')
