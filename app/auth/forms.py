from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('Epasts', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Parole', validators=[DataRequired()])
    remember_me = BooleanField('Atcerēties mani')
    sumbit = SubmitField('Pieslēgties')
