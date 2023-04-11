from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    remember_me = BooleanField('Atcerēties mani')
    sumbit = SubmitField('Pieslēgties')



class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Pašreizēja parole', validators=[DataRequired()])
    password = PasswordField(
        'Jaunā parole', validators=[
            DataRequired(), EqualTo('password2', message='Parolēm jāsakrīt')])
    password2 = PasswordField(
        'Apstiprini jauno paroli', validators=[DataRequired()])
    submit = SubmitField('Nomainīt paroli')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Atiestatīt paroli')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Jaunā parole', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Apstiprini paroli', validators=[DataRequired()])
    submit = SubmitField('Atiestatīt paroli')


class ChangeEmailForm(FlaskForm):
    email = StringField('Jaunā e-pasta adrese', validators=[DataRequired(), Length(1, 64),
                                                            Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    submit = SubmitField('Nomainīt e-pasta adresi')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Šāda e-pasta adrese jau ir reģistrēta')
