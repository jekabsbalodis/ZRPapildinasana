from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from .forms import DownloadForm
from . import filePrepare
from ..downloadData import download_register, download_register_delta, download_doping_substances


@filePrepare.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    form = DownloadForm()
    if form.validate_on_submit():
        dateFrom = form.dateFrom.data
        download_register()
        download_register_delta(dateFrom=dateFrom)
        download_doping_substances()
        flash('Faili lejuplādēti')
        return redirect(url_for('filePrepare.checkMedication'))
    return render_template('filePrepare/download.html', form=form)

@filePrepare.route('/checkMedication', methods=['GET', 'POST'])
@login_required
def checkMedication():
    return render_template('filePrepare/checkMedication.html')
