'''View functions for registration model'''
import string
import secrets
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import reg
from .. import db
from ..models import User
from ..email import send_email
from .forms import RegistrationForm
from ..decorators import admin_required


@reg.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    '''Function for registering new user for ZRApp'''
    form = RegistrationForm()
    if form.validate_on_submit():
        symbols = string.ascii_letters + string.digits
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=''.join(secrets.choice(symbols) for i in range(16)))
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Apstiprini savu lietotāja kontu',
                   'auth/email/confirm', user=user, token=token)
        flash('Uz Jūsu e-pasta adresi nosūtīts aicinājums apstiprināt to!')
        return redirect(url_for('main.index'))
    return render_template('reg/register.html', form=form)
