'''View functions to pages for preparing file with information about medications use in sports'''
import csv
from datetime import date, timedelta
from flask_login import login_required
from flask import render_template, flash, redirect, url_for, request, current_app
from .forms import DownloadForm, ReviewMedicationForm, UploadDataGovLVForm, UploadZVAForm
from . import file_prepare
from .. import db
from ..download_data import download_register, download_register_delta, download_doping_substances
from ..upload_data import upload_data_gov_lv, upload_zva
from ..models import AddedMedication, NotesFields
from ..last_update import last_update


@file_prepare.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    '''Function for data download view'''
    form = DownloadForm()
    if form.validate_on_submit():
        date_from = form.dateFrom.data
        date_to = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        AddedMedication.insert_medication(
            download_register_delta(date_from=date_from, date_to=date_to),
            download_register())
        download_doping_substances()
        with open('.lastUpdate', 'w', encoding='utf-8') as f:
            f.write(date.today().strftime('%Y-%m-%d'))
        flash('Faili lejuplādēti')
        return redirect(url_for('file_prepare.review_medication'))
    return render_template('file_prepare/download.html',
                           form=form,
                           last_update=last_update().strftime('%Y-%m-%d'))


@file_prepare.route('/review_medication')
@login_required
def review_medication():
    '''Function for products that need reviewing'''
    added_medications = AddedMedication.query.all()
    count = len(added_medications)
    unchecked_medications = AddedMedication.query.filter_by(
        userChecked=False).all()
    count_unchecked = len(unchecked_medications)
    return render_template('file_prepare/review_medication.html',
                           added_medications=added_medications,
                           count=count,
                           count_unchecked=count_unchecked)


@file_prepare.route('/check_medication', methods=['GET', 'POST'])
@login_required
def check_medication():
    '''Function for providing information about medication use in sports'''
    reg_number = request.args.get('reg_number')
    form = ReviewMedicationForm()
    medication = AddedMedication.query.filter_by(regNumber=reg_number).first()
    atc_code = medication.atcCode
    pharmaceutical_form = medication.form
    if medication.regNumber.startswith('EU/'):
        bulk_edit = True
    else:
        bulk_edit = False
    notes_by_form = NotesFields.query.filter_by(
        uniqueIdentifier=f'{atc_code}_{pharmaceutical_form}').first()
    notes_by_atc = NotesFields.query.filter_by(atcCode=atc_code).first()
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
            reg_no = medication.regNumber.split('/')
            reg_no.pop()
            reg_no_str = '/'.join(str(x) for x in reg_no)
            needed_form = medication.form
            medications = AddedMedication.query.filter(
                AddedMedication.regNumber.contains(reg_no_str),
                AddedMedication.form == needed_form).all()
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
        return redirect(url_for('file_prepare.review_medication', _anchor=medication.regNumber))
    return render_template('file_prepare/check_medication.html',
                           form=form, medication=medication, notes_by_form=notes_by_form, notes_by_atc=notes_by_atc, bulk_edit=bulk_edit)


@file_prepare.route('/upload_review')
@login_required
def upload_review():
    '''Function to review the provided information for each medication'''
    AddedMedication.write_information('antidopinga_vielas.csv')
    with open(date.today().strftime('%Y%m%d') + '.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        return render_template('file_prepare/upload_review.html', csv=reader)


@file_prepare.route('/upload_finished', methods=['GET', 'POST'])
@login_required
def upload_finished():
    '''Function to upload the data to servers'''
    zva_form = UploadZVAForm()
    data_gov_lv_form = UploadDataGovLVForm()
    if zva_form.submitZVA.data and zva_form.validate():
        upload_zva(user_name=current_app.config['ZVA_USER_NAME'],
                   password=current_app.config['ZVA_PASSWORD'],
                   ftp_address=current_app.config['ZVA_FTP_ADDRESS'],
                   ftp_port=int(current_app.config['ZVA_FTP_PORT']),
                   file_name=date.today().strftime('%Y%m%d') + '_antidopinga_vielas.csv')
        flash('Dati ZVA serverī augšuplādēti')
    if data_gov_lv_form.submitDataGovLV.data and data_gov_lv_form.validate():
        upload_data_gov_lv(resource_id=current_app.config['DATA_GOV_LV_RESOURCE_ID'],
                           api_key=current_app.config['DATA_GOV_LV_API_KEY'],
                           file_name=date.today().strftime('%Y%m%d') + '_antidopinga_vielas.csv')
        flash('Dati data.gov.lv serverī augšuplādēti')
    return render_template('med_search/upload_finished.html',
                           zva_form=zva_form,
                           data_gov_lv_form=data_gov_lv_form)
