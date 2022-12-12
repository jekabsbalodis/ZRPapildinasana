from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    remember_me = BooleanField('Atcerēties mani')
    sumbit = SubmitField('Pieslēgties')


class RegistrationForm(FlaskForm):
    email = StringField(
        'E-pasts', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Lietotāja vārds', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or ''underscores')])
    password = PasswordField('Parole', validators=[
                             DataRequired(), EqualTo('password2', message='Paroles nesakrīt')])
    password2 = PasswordField('Apstiprini paroli', validators=[DataRequired()])
    submit = SubmitField('Reģistrēties')

    def validate_email(self, field):
        app = current_app._get_current_object()
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Šāds e-pasts jau ir reģistrēts')
        email_domain = field.data.split('@')[-1]
        if email_domain not in app.config['ALLOWED_REG_DOMAINS']:
            raise ValidationError('Jums nav tiesību izveidot lietotāja kontu')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Šāds lietotāja vārds jau ir reģistrēts')