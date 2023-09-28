from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField(
        'E-pasts', validators=[DataRequired(), Length(1, 64), Email('Ievadīta nederīga e-pasta adrese')])
    username = StringField('Lietotāja vārds', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Lietotāja vārdam jāsastāv tikai no burtiem, cipariem, punkta vai apakšvītras')])
    submit = SubmitField('Reģistrēt')

    def validate_email(self, field):
        app = current_app._get_current_object()
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Šāds e-pasts jau ir reģistrēts')
        email_domain = field.data.split('@')[-1]

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Šāds lietotāja vārds jau ir reģistrēts')
