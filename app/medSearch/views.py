from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from . import medSearch
from .forms import AtcSearchForm
from ..filePrepare.forms import ReviewMedicationForm, UploadZVAForm, UploadDataGovLVForm
from ..models import SearchedMedication, NotesFields
from ..downloadData import download_register, download_doping_substances
from ..uploadData import upload_zva, upload_data_gov_lv
from .. import db
from datetime import date
import csv


@medSearch.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = AtcSearchForm()
    download_doping_substances()
    if form.validate_on_submit():
        SearchedMedication.insert_medication(download_register(), form.atcCode.data.upper())
        flash('Meklēšana pēc ATĶ koda veikta')
        return redirect(url_for('medSearch.reviewMedication'))
    return render_template('medSearch/search.html', form=form)


@medSearch.route('/reviewMedication', methods=['GET', 'POST'])
@login_required
def reviewMedication():
    searchedMedications = SearchedMedication.query.all()
    count = len(searchedMedications)
    uncheckedMedications = SearchedMedication.query.filter_by(userChecked=False).all()
    countUnchecked = len(uncheckedMedications)
    return render_template('medSearch/reviewMedication.html',
                           searchedMedications=searchedMedications,
                           count=count,
                           countUnchecked=countUnchecked)


@medSearch.route('/checkMedication', methods=['GET', 'POST'])
@login_required
def checkMedication():
    regNumber = request.args.get('regNumber')
    form = ReviewMedicationForm()
    medication = SearchedMedication.query.filter_by(regNumber=regNumber).first()
    atcCode = medication.atcCode
    if medication.regNumber.startswith('EU/'):
        bulkEdit = True
    else:
        bulkEdit = False
    notes = NotesFields.query.filter_by(atcCode=atcCode).first()
    if form.validate_on_submit():
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
            medication.userChecked = True
            db.session.commit()
        if form.bulkInclude.data:
            regNo = medication.regNumber.split('/')
            regNo.pop()
            regNoStr = '/'.join(str(x) for x in regNo)
            neededForm = medication.form
            medications = SearchedMedication.query.filter(
                SearchedMedication.regNumber.contains(regNoStr), SearchedMedication.form == neededForm).all()
            for medication in medications:
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
                medication.userChecked = True
                db.session.commit()
        if form.notInclude.data:
            medication.include = False
            medication.userChecked = True
            db.session.commit()
        return redirect(url_for('medSearch.reviewMedication'))
    return render_template('medSearch/checkMedication.html',
                           form=form, medication=medication, notes=notes, bulkEdit=bulkEdit)


@medSearch.route('/uploadReview', methods=['GET', 'POST'])
@login_required
def uploadReview():
    SearchedMedication.write_information('antidopinga_vielas.csv')
    with open(date.today().strftime('%Y%m%d')+'.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        return render_template('medSearch/uploadReview.html', csv=reader)


@medSearch.route('/uploadFinished', methods=['GET', 'POST'])
@login_required
def uploadFinished():
    zvaForm = UploadZVAForm()
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
    return render_template('medSearch/uploadFinished.html', zvaForm=zvaForm, dataGovLVForm=dataGovLVForm)
