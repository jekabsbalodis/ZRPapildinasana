from flask import render_template, flash, redirect, url_for
from . import main
from..downloadData import download_register
from .forms import DownloadForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/download', methods=['GET', 'POST'])
# @login_required
# @admin_required
def download():
    form = DownloadForm()
    if form.validate_on_submit():
        download_register('tests')
        flash('fails lejuplādēts')
        return redirect(url_for('main.index'))
    return render_template('download/download.html', form=form)