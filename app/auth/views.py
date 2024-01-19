'''View functions for pages related to authentication'''
from flask import render_template, redirect, request, url_for, flash
from flask_login import fresh_login_required, login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    '''Redirect unconfirmed users'''
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    '''View for users who are unconfirmed'''
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Function for login view'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Nepareizs lietotāja vārds vai parole')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    '''Function for user logout'''
    logout_user()
    flash('Jūs esat atslēdzies no sistēmas')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    '''Function for user confirmation view'''
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Paldies, ka apstiprināji savu e-pasta adresi!')
    else:
        flash('Saite e-pasta adreses apstiprināšanai ir nederīga vai tai ir beidzies termiņš')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    '''Function to request confirmation resend'''
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Apstiprini savu lietotāja kontu',
               'auth/email/confirm',
               user=current_user, token=token)
    flash('Uz Jūsu e-pasta adresi nosūtīts jauns aicinājums apstiprināt to!')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def change_password():
    '''Function for user password change view'''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Jūsu parole ir nomainīta')
            return redirect(url_for('main.index'))
        else:
            flash('Nederīga parole')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    '''Function for password reset request view'''
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,
                       'Atiestatīt paroli',
                       'auth/email/reset_password',
                       user=user,
                       token=token)
        flash('Jums ir nosūtīts e-pasts ar instrukciju, kā atiestatīt Jūsu paroli')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    '''Function for password reset form'''
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Jūsu parole ir atiestatīta')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def change_email_request():
    '''Function for entering new email before changing it'''
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Apstiprini e-pasta adresi',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash(
                'Jums ir nosūtīts e-pasts ar instrukciju, kā apstiprināt jauno e-pasta adresi')
            return redirect(url_for('main.index'))
        else:
            flash('Nepareiza e-pasta adrese vai parole')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    '''Function for changing email in database'''
    if current_user.change_email(token):
        db.session.commit()
        flash('Jūsu e-pasta adrese ir nomainīta')
    else:
        flash('Nederīgs pieprasījums')
    return redirect(url_for('main.index'))
