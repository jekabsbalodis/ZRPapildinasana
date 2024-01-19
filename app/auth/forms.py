'''Forms for authentication model'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    '''Form for user login view'''
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    remember_me = BooleanField('Atcerēties mani')
    submit = SubmitField('Pieslēgties')



class ChangePasswordForm(FlaskForm):
    '''Form for user password change view'''
    old_password = PasswordField(
        'Pašreizēja parole', validators=[DataRequired()])
    password = PasswordField(
        'Jaunā parole', validators=[
            DataRequired(), EqualTo('password2', message='Parolēm jāsakrīt')])
    password2 = PasswordField(
        'Apstiprini jauno paroli', validators=[DataRequired()])
    submit = SubmitField('Nomainīt paroli')


class PasswordResetRequestForm(FlaskForm):
    '''Form for user password reset request view'''
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Atiestatīt paroli')


class PasswordResetForm(FlaskForm):
    '''Form for user password reset view'''
    password = PasswordField('Jaunā parole', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Apstiprini paroli', validators=[DataRequired()])
    submit = SubmitField('Atiestatīt paroli')


class ChangeEmailForm(FlaskForm):
    '''Form for user email change view'''
    email = StringField('Jaunā e-pasta adrese', validators=[DataRequired(), Length(1, 64),
                                                            Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    submit = SubmitField('Nomainīt e-pasta adresi')

    def validate_email(self, field):
        '''Function for email validation'''
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Šāda e-pasta adrese jau ir reģistrēta')
