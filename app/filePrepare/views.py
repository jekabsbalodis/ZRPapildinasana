from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from .forms import DownloadForm
from . import filePrepare
from .. import db
from ..downloadData import download_register, download_register_delta, download_doping_substances
from ..models import AddedMedication
import xml.etree.ElementTree as ET



@filePrepare.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    form = DownloadForm()
    if form.validate_on_submit():
        dateFrom = form.dateFrom.data
        # download_register()
        download_register_delta(dateFrom=dateFrom)
        download_doping_substances()
        flash('Faili lejuplādēti')
        return redirect(url_for('filePrepare.checkMedication'))
    return render_template('filePrepare/download.html', form=form)

@filePrepare.route('/checkMedication', methods=['GET', 'POST'])
@login_required
def checkMedication():
    with open('delta.xml', encoding='utf-8') as file:
        allStuff = ET.parse(file)
    products = allStuff.findall('meds/med')
    for product in products:
        name = product.findtext('med_name')
        regNumber = product.findtext('reg_number')
        m = AddedMedication(name=name, regNumber=regNumber)
        db.session.add(m)
        db.session.commit()
    return render_template('filePrepare/checkMedication.html')
