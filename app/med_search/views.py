'''View functions for page to prepare information for searched medication'''
from datetime import date
import csv
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from . import med_search
from .forms import AtcSearchForm, NameSearchForm, RegSearchForm
from ..file_prepare.forms import ReviewMedicationForm, UploadZVAForm, UploadDataGovLVForm
from ..models import SearchedMedication, NotesFields
from ..download_data import download_register, download_doping_substances
from ..upload_data import upload_zva, upload_data_gov_lv
from .. import db


@med_search.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    '''Function for performing search for medication'''
    form_atc = AtcSearchForm()
    form_name = NameSearchForm()
    form_reg = RegSearchForm()
    download_doping_substances()
    if form_atc.searchAtcCode.data and form_atc.validate():
        SearchedMedication.insert_medication(
            download_register(),
            search_term=form_atc.atcCode.data.upper())
        flash('Meklēšana pēc ATĶ koda veikta')
        return redirect(url_for('med_search.review_medication'))
    if form_name.searchName.data and form_name.validate():
        SearchedMedication.insert_medication(
            download_register(),
            search_term=form_name.name.data.lower())
        flash('Meklēšana pēc aktīvas vielas nosaukuma veikta')
        return redirect(url_for('med_search.review_medication'))
    if form_reg.searchRegNumber.data and form_reg.validate():
        SearchedMedication.insert_medication(
            download_register(),
            search_term=form_reg.regNumber.data.upper())
        flash('Meklēšana pēc reģistrācijas numura veikta')
        return redirect(url_for('med_search.review_medication'))
    return render_template('med_search/search.html',
                           form_atc=form_atc,
                           form_name=form_name,
                           form_reg=form_reg)


@med_search.route('/review_medication')
@login_required
def review_medication():
    '''Function for products that need reviewing'''
    searched_medications = SearchedMedication.query.all()
    count = len(searched_medications)
    unchecked_medications = SearchedMedication.query.filter_by(
        userChecked=False).all()
    count_unchecked = len(unchecked_medications)
    return render_template('med_search/review_medication.html',
                           searched_medications=searched_medications,
                           count=count,
                           count_unchecked=count_unchecked)


@med_search.route('/check_medication', methods=['GET', 'POST'])
@login_required
def check_medication():
    '''Function for providing information about medication use in sports'''
    reg_number = request.args.get('reg_number')
    with open('antidopinga_vielas.csv', encoding='utf-8') as f:
        if reg_number in f.read():
            admin_required = True
        else:
            admin_required = False
    form = ReviewMedicationForm()
    medication = SearchedMedication.query.filter_by(
        regNumber=reg_number).first()
    atc_code = medication.atcCode
    if medication.regNumber.startswith('EU/'):
        bulk_edit = True
    else:
        bulk_edit = False
    notes = NotesFields.query.filter_by(atcCode=atc_code).first()
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
            medications = SearchedMedication.query.filter(
                SearchedMedication.regNumber.contains(reg_no_str),
                SearchedMedication.form == needed_form).all()
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
        return redirect(url_for('med_search.review_medication', _anchor=medication.regNumber))
    return render_template('med_search/check_medication.html',
                           form=form, medication=medication,
                           notes=notes,
                           bulk_edit=bulk_edit,
                           admin_required=admin_required)


@med_search.route('/upload_review')
@login_required
def upload_review():
    '''Function to review the provided information for each medication'''
    SearchedMedication.write_information('antidopinga_vielas.csv')
    with open(date.today().strftime('%Y%m%d')+'.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        return render_template('med_search/upload_review.html', csv=reader)


@med_search.route('/upload_finished', methods=['GET', 'POST'])
@login_required
def upload_finished():
    '''Function to upload the data to servers'''
    zva_form = UploadZVAForm()
    data_gov_lv_form = UploadDataGovLVForm()
    if zva_form.submitZVA.data and zva_form.validate():
        upload_zva(user_name=zva_form.userName.data,
                   password=zva_form.passWord.data,
                   ftp_address=zva_form.ftpAddress.data,
                   ftp_port=zva_form.ftpPort.data,
                   file_name=date.today().strftime('%Y%m%d')+'_antidopinga_vielas.csv')
        flash('Dati ZVA serverī augšuplādēti')
    if data_gov_lv_form.submitDataGovLV.data and data_gov_lv_form.validate():
        upload_data_gov_lv(resource_id=data_gov_lv_form.resourceID.data,
                           api_key=data_gov_lv_form.apiKey.data,
                           file_name=date.today().strftime('%Y%m%d')+'_antidopinga_vielas.csv')
        flash('Dati data.gov.lv serverī augšuplādēti')
    return render_template('med_search/upload_finished.html',
                           zva_form=zva_form,
                           data_gov_lv_form=data_gov_lv_form)
