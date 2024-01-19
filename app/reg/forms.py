'''Forms for registration model'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User


class RegistrationForm(FlaskForm):
    '''Form for registering new user in ZRApp'''
    email = StringField('E-pasts',
                        validators=[DataRequired(),
                                    Length(1, 64),
                                    Email('Ievadīta nederīga e-pasta adrese')])
    username = StringField('Lietotāja vārds',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Lietotāja vārdam jāsastāv tikai no'
                                               ' burtiem, cipariem, punkta vai apakšvītras')])
    submit = SubmitField('Reģistrēt')

    def validate_email(self, field):
        '''Function for email validation'''
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Šāds e-pasts jau ir reģistrēts')

    def validate_username(self, field):
        '''Function for username validation'''
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Šāds lietotāja vārds jau ir reģistrēts')
