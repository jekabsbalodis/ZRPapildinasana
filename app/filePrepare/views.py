from flask_login import login_required
from flask import render_template, flash, redirect, url_for, request
import requests
from .forms import DownloadForm, ReviewMedicationForm, UploadDataGovLVForm, UploadZVAFrom
from . import filePrepare
from .. import db
from ..downloadData import download_register, download_register_delta, download_doping_substances
from ..uploadData import upload_data_gov_lv, upload_zva
from ..models import AddedMedication, NotesFields
import csv
from datetime import date
from datetime import timedelta


@filePrepare.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    form = DownloadForm()
    url = 'https://data.gov.lv/dati/lv/api/3/action/package_show?id=medikamenti-kas-satur-dopinga-vielas'
    data = requests.get(url).json()
    lastUpdate = data.get('result').get('resources')[
        0].get('last_modified')[:10]
    if form.validate_on_submit():
        dateFrom = form.dateFrom.data
        dateTo = (date.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
        AddedMedication.insert_medication(
            download_register_delta(dateFrom=dateFrom, dateTo=dateTo), download_register())
        download_doping_substances()
        flash('Faili lejuplādēti')
        return redirect(url_for('filePrepare.reviewMedication'))
    return render_template('filePrepare/download.html', form=form, lastUpdate=lastUpdate)


@filePrepare.route('/reviewMedication', methods=['GET', 'POST'])
@login_required
def reviewMedication():
    addedMedications = AddedMedication.query.all()
    count = len(addedMedications)
    uncheckedMedications = AddedMedication.query.filter_by(
        userChecked=False).all()
    countUnchecked = len(uncheckedMedications)
    return render_template('filePrepare/reviewMedication.html',
                           addedMedications=addedMedications,
                           count=count,
                           countUnchecked=countUnchecked)


@filePrepare.route('/checkMedication', methods=['GET', 'POST'])
@login_required
def checkMedication():
    regNumber = request.args.get('regNumber')
    form = ReviewMedicationForm()
    medication = AddedMedication.query.filter_by(regNumber=regNumber).first()
    atcCode = medication.atcCode
    notes = NotesFields.query.filter_by(atcCode=atcCode).first()
    if form.validate_on_submit():
        medication.userChecked = True
        if form.include.data:
            medication.prohibitedOUTCompetition = form.prohibitedOUTCompetition.data
            medication.prohibitedINCompetition = form.prohibitedINCompetition.data
            medication.prohibitedClass = form.prohibitedClass.data.upper()
            medication.notesLV = form.notesLV.data
            medication.notesEN = form.notesEN.data
            medication.sportsINCompetitionLV = form.sportsINCompetitionLV.data
            medication.sportsINCompetitionEN = form.sportsINCompetitionEN.data
            medication.sportsOUTCompetitionLV = form.sportsOUTCompetitionLV.data
            medication.sportsOUTCompetitionEN = form.sportsOUTCompetitionEN.data
            medication.include = True
        if form.notInclude.data:
            medication.include = False
        db.session.commit()
        return redirect(url_for('filePrepare.reviewMedication'))
    return render_template('filePrepare/checkMedication.html', form=form, medication=medication, notes=notes)


@filePrepare.route('/uploadReview', methods=['GET', 'POST'])
@login_required
def uploadReview():
    AddedMedication.write_information('antidopinga_vielas.csv')
    with open(date.today().strftime('%Y%m%d')+'.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        return render_template('filePrepare/uploadReview.html', csv=reader)


@filePrepare.route('/uploadFinished', methods=['GET', 'POST'])
@login_required
def uploadFinished():
    zvaForm = UploadZVAFrom()
    dataGovLVForm = UploadDataGovLVForm()
    if zvaForm.submitZVA.data and zvaForm.validate():
        upload_zva(userName=zvaForm.userName.data,
                   passWord=zvaForm.passWord.data,
                   ftpAddress=zvaForm.ftpAddress.data,
                   ftpPort=zvaForm.ftpPort.data,
                   fileName=date.today().strftime('%Y%m%d')+'_antidopinga_vielas.csv')
        flash('Dati ZVA serverī augšuplādēti')
    if dataGovLVForm.submitDataGovLV.data and dataGovLVForm.validate():
        upload_data_gov_lv(resourceID=dataGovLVForm.resourceID.data,
                           apiKey=dataGovLVForm.apiKey.data,
                           fileName=date.today().strftime('%Y%m%d')+'_antidopinga_vielas.csv')
        flash('Dati data.gov.lv serverī augšuplādēti')
    return render_template('filePrepare/uploadFinished.html', zvaForm=zvaForm, dataGovLVForm=dataGovLVForm)
