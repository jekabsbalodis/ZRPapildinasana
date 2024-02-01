'''Forms for preparing file with information about medication use in sports'''
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField, \
    StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length
from ..last_update import last_update


class DownloadForm(FlaskForm):
    '''Form to select date from which to search for newly included medication'''
    dateFrom = DateField('No kura datuma pārskatīt medikamentus?',
                         default=last_update,
                         format='%Y-%m-%d',
                         validators=[DataRequired()])
    #  render_kw={'oninvalid': 'this.setCustomValidity("Ievadi datumu")'})
    #  Atribūts formas laukam, lai nomainītu attēlojamo tekstu,
    #  ja tiek mēģināts iesniegt tukšu lauku
    submit = SubmitField('Apstiprināt')


class ReviewMedicationForm(FlaskForm):
    '''Form to provide information about medicines use in sports'''
    prohibitedOUTCompetition = SelectField(
        'Vai medikaments ir aizliegts ārpus sacensībām?',
        choices=['Jā', 'Nē', 'Jā*', 'Ar nosacījumu'],
        default='Nē')
    prohibitedINCompetition = SelectField(
        'Vai medikaments ir aizliegts sacensību laikā?',
        choices=['Jā', 'Nē', 'Jā*', 'Ar nosacījumu'],
        default='Nē')
    prohibitedClass = StringField(
        'Kurai Aizliegto vielu un metožu saraksta klasei medikaments pieder?',
        validators=[Length(max=10)])
    notesLV = TextAreaField('Piezīmes par medikamenta lietošanu')
    notesEN = TextAreaField('Norādi šo informāciju angliski')
    sportsINCompetitionLV = TextAreaField(
        label='Ja medikaments aizliegts tikai noteiktos'
        ' sporta veidos sacensību laikā, norādi šos sporta veidus')
    sportsINCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    sportsOUTCompetitionLV = TextAreaField(
        label='Ja medikaments aizliegts tikai noteiktos'
        ' sporta veidos ārpus sacensībām, norādi šos sporta veidus')
    sportsOUTCompetitionEN = TextAreaField('Norādi šo informāciju angliski')
    include = SubmitField('Iekļaut')
    bulkInclude = SubmitField('Iekļaut visus līdzīgus medikamentus')
    notInclude = SubmitField('Neiekļaut nododamajos datos')


class UploadZVAForm(FlaskForm):
    '''Form to provide credentials to upload prepared file'''
    # userName = StringField('Lietotāja vārds', validators=[DataRequired()])
    # passWord = PasswordField('Parole', validators=[DataRequired()])
    # ftpAddress = StringField('Servera adrese', validators=[DataRequired()])
    # ftpPort = IntegerField('Servera ports', validators=[DataRequired()])
    submitZVA = SubmitField('Augšuplādēt')


class UploadDataGovLVForm(FlaskForm):
    '''Form to provide credentials to upload prepared file'''
    # resourceID = StringField('Resursa ID numurs', validators=[DataRequired()])
    # apiKey = PasswordField('api atslēga', validators=[DataRequired()])
    submitDataGovLV = SubmitField('Augšuplādēt')
