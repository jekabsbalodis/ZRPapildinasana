'''Defining models for ZRApp'''
import xml.etree.ElementTree as ET
import csv
from datetime import date
import shutil
import fileinput
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from . import db, login_manager


class Permission:
    '''Permissions for ZRApp user roles'''
    WRITE = 1
    ADMIN = 2


class Role(db.Model):
    '''Model for ZRApp user roles'''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        '''Insert user roles when creating new users'''
        roles = {
            'User': [Permission.WRITE],
            'Administrator': [Permission.WRITE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        '''Add new permissions to user'''
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        '''Remove permissions from user'''
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        '''Remove all permission from user'''
        self.permissions = 0

    def has_permission(self, perm):
        '''Check if user has certain permissions'''
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    '''Model for ZRApp users'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ZRAPP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('parole nav nolasāms lauks')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''Verifiy user's password'''
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        '''Generate token for user confirmation'''
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
        '''Verify user confirmation function works'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self):
        '''Generate token for users' password reset'''
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
        '''Reset users' password'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email):
        '''Generate token for users' email change'''
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token, expiration=3600):
        '''Change user's email'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AddedMedication(db.Model):
    '''Model for medication that has been recently included in human medicines' register'''
    __tablename__ = 'added_medication'
    id = db.Column(db.Integer, primary_key=True)
    atcCode = db.Column(db.String(10))
    name = db.Column(db.Text)
    regNumber = db.Column(db.String(20))
    form = db.Column(db.Text)
    activeSubstance = db.Column(db.Text)
    include = db.Column(db.Boolean, default=False)
    userChecked = db.Column(db.Boolean, default=False)
    prohibitedOUTCompetition = db.Column(db.String(15))
    prohibitedINCompetition = db.Column(db.String(15))
    prohibitedClass = db.Column(db.String(10))
    notesLV = db.Column(db.Text)
    sportsINCompetitionLV = db.Column(db.Text)
    sportsOUTCompetitionLV = db.Column(db.Text)
    notesEN = db.Column(db.Text)
    sportsINCompetitionEN = db.Column(db.Text)
    sportsOUTCompetitionEN = db.Column(db.Text)

    @staticmethod
    def insert_medication(delta_file, file):
        '''Function to create new products in database'''
        AddedMedication.query.delete()  # Start with an empty table to avoid duplicates
        db.session.commit()
        with open(delta_file, encoding='utf-8') as df:
            all_stuff_delta = ET.parse(df)
        products_delta = all_stuff_delta.findall('meds/med')
        with open(file, encoding='utf-8') as f:
            all_stuff = ET.parse(f)
        products = all_stuff.findall('products/product')
        products_delta_checked = []
        for product_delta in products_delta:
            for product in products:
                if product_delta.findtext('reg_number') in products_delta_checked:
                    continue
                if product_delta.findtext('reg_number') == product.findtext('authorisation_no'):
                    name = product_delta.findtext('med_name')
                    reg_number = product_delta.findtext('reg_number')
                    atc_code = product.findtext('atc_code')
                    form = product.findtext('pharmaceutical_form_lv')
                    active_substance = product.findtext('active_substance')
                    m = AddedMedication(
                        name=name,
                        regNumber=reg_number,
                        atcCode=atc_code,
                        form=form,
                        activeSubstance=active_substance)
                    db.session.add(m)
                    db.session.commit()
                    products_delta_checked.append(
                        product_delta.findtext('reg_number'))

    @staticmethod
    def write_information(file_name):
        '''Function to write information to .csv file'''
        new_file_name = date.today().strftime('%Y%m%d')+'_'+file_name
        shutil.copyfile(file_name, new_file_name)
        with open(date.today().strftime('%Y%m%d')+'.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel', delimiter=',')
            medications = AddedMedication.query.all()
            for medication in medications:
                if medication.include is False:
                    continue
                writer.writerow([medication.name,
                                 medication.regNumber,
                                 medication.form,
                                 medication.activeSubstance,
                                 medication.prohibitedOUTCompetition,
                                 medication.prohibitedINCompetition,
                                 medication.prohibitedClass,
                                 medication.notesLV,
                                 medication.sportsINCompetitionLV,
                                 medication.sportsOUTCompetitionLV,
                                 medication.notesEN,
                                 medication.sportsINCompetitionEN,
                                 medication.sportsOUTCompetitionEN])
        with open(new_file_name, 'a', encoding='utf-8', newline='') as f:
            input_lines = fileinput.input(
                date.today().strftime('%Y%m%d')+'.csv')
            f.writelines(input_lines)
        df = pd.read_csv(new_file_name)
        df = df.drop_duplicates(subset=['authorisation_no'], keep='last')
        df.to_csv(new_file_name, index=False)


class SearchedMedication(db.Model):
    '''Model for medication that has been added by search'''
    __tablename__ = 'searched_medication'
    id = db.Column(db.Integer, primary_key=True)
    atcCode = db.Column(db.String(10))
    name = db.Column(db.Text)
    regNumber = db.Column(db.String(20))
    form = db.Column(db.Text)
    activeSubstance = db.Column(db.Text)
    include = db.Column(db.Boolean, default=False)
    userChecked = db.Column(db.Boolean, default=False)
    doping = db.Column(db.Boolean, default=False)
    prohibitedOUTCompetition = db.Column(db.String(15))
    prohibitedINCompetition = db.Column(db.String(15))
    prohibitedClass = db.Column(db.String(10))
    notesLV = db.Column(db.Text)
    sportsINCompetitionLV = db.Column(db.Text)
    sportsOUTCompetitionLV = db.Column(db.Text)
    notesEN = db.Column(db.Text)
    sportsINCompetitionEN = db.Column(db.Text)
    sportsOUTCompetitionEN = db.Column(db.Text)

    @staticmethod
    def insert_medication(file, search_term):
        '''Function to create new products in database'''
        SearchedMedication.query.delete()  # Start with an empty table to avoid duplicates
        db.session.commit()
        with open(file, encoding='utf-8') as f:
            all_stuff = ET.parse(f)
        products = all_stuff.findall('products/product')
        for product in products:
            if SearchedMedication.query.filter_by(
                    regNumber=product.findtext('authorisation_no')).first():
                continue
            if (search_term in product.findtext('atc_code')) \
                    or (search_term in product.findtext('active_substance').lower()) \
                    or (search_term in product.findtext('authorisation_no')):
                name = product.findtext('medicine_name')
                reg_number = product.findtext('authorisation_no')
                atc_code = product.findtext('atc_code')
                form = product.findtext('pharmaceutical_form_lv')
                active_substance = product.findtext('active_substance')
                m = SearchedMedication(name=name,
                                       regNumber=reg_number,
                                       atcCode=atc_code,
                                       form=form,
                                       activeSubstance=active_substance)
                db.session.add(m)
                db.session.commit()
        searched_med = SearchedMedication.query.all()
        for med in searched_med:
            with open('antidopinga_vielas.csv', encoding='utf-8') as df:
                df_csv = csv.reader(df)
                for line in df_csv:
                    if med.regNumber in line:
                        med.include = False
                        med.userChecked = True
                        med.doping = True
                        med.prohibitedOUTCompetition = line[4]
                        med.prohibitedINCompetition = line[5]
                        med.prohibitedClass = line[6]
                        med.notesLV = line[7]
                        med.sportsINCompetitionLV = line[8]
                        med.sportsOUTCompetitionLV = line[9]
                        med.notesEN = line[10]
                        med.sportsINCompetitionEN = line[11]
                        med.sportsOUTCompetitionEN = line[12]
                        db.session.commit()

    @staticmethod
    def write_information(file_name):
        '''Function to write information to .csv file'''
        new_file_name = date.today().strftime('%Y%m%d')+'_'+file_name
        shutil.copyfile(file_name, new_file_name)
        with open(date.today().strftime('%Y%m%d')+'.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel', delimiter=',')
            medications = SearchedMedication.query.all()
            for medication in medications:
                if medication.include is False:
                    continue
                writer.writerow([medication.name,
                                 medication.regNumber,
                                 medication.form,
                                 medication.activeSubstance,
                                 medication.prohibitedOUTCompetition,
                                 medication.prohibitedINCompetition,
                                 medication.prohibitedClass,
                                 medication.notesLV,
                                 medication.sportsINCompetitionLV,
                                 medication.sportsOUTCompetitionLV,
                                 medication.notesEN,
                                 medication.sportsINCompetitionEN,
                                 medication.sportsOUTCompetitionEN])
        with open(new_file_name, 'a', encoding='utf-8', newline='') as f:
            input_lines = fileinput.input(
                date.today().strftime('%Y%m%d')+'.csv')
            f.writelines(input_lines)
        df = pd.read_csv(new_file_name)
        df = df.drop_duplicates(subset=['authorisation_no'], keep='last')
        df.to_csv(new_file_name, index=False)


class NotesFields(db.Model):
    '''Model for database with notes about information on medications' use in sports'''
    __tablename__ = 'notes_fields'
    id = db.Column(db.Integer, primary_key=True)
    atcCode = db.Column(db.String(10), unique=True)
    prohibitedOUTCompetition = db.Column(db.String(15))
    prohibitedINCompetition = db.Column(db.String(15))
    prohibitedClass = db.Column(db.String(10))
    notesLV = db.Column(db.Text)
    sportsINCompetitionLV = db.Column(db.Text)
    sportsOUTCompetitionLV = db.Column(db.Text)
    notesEN = db.Column(db.Text)
    sportsINCompetitionEN = db.Column(db.Text)
    sportsOUTCompetitionEN = db.Column(db.Text)

    @staticmethod
    def update_notes(drug_register, doping_register):
        '''Function to update the databes'''
        with open(drug_register, encoding='utf-8') as dr:
            all_stuff = ET.parse(dr)
        products = all_stuff.findall('products/product')
        with open(doping_register, encoding='utf-8', newline='') as dr:
            reader = csv.reader(dr, dialect='excel', delimiter=',')
            rows = list(reader)
            for product in products:
                authorisation_no = product.findtext('authorisation_no')
                atc_code = product.findtext('atc_code')
                if NotesFields.query.filter_by(atcCode=atc_code).first():
                    continue
                for row in rows:
                    if authorisation_no in row:
                        prohibited_out = row[4]
                        prohibited_in = row[5]
                        prohibited_class = row[6]
                        notes_lv = row[7]
                        sports_in = row[8]
                        sports_out = row[9]
                        notes_en = row[10]
                        sports_in_en = row[11]
                        sports_out_en = row[12]
                        m = NotesFields(atcCode=atc_code,
                                        prohibitedOUTCompetition=prohibited_out,
                                        prohibitedINCompetition=prohibited_in,
                                        prohibitedClass=prohibited_class,
                                        notesLV=notes_lv,
                                        sportsINCompetitionLV=sports_in,
                                        sportsOUTCompetitionLV=sports_out,
                                        notesEN=notes_en,
                                        sportsINCompetitionEN=sports_in_en,
                                        sportsOUTCompetitionEN=sports_out_en)
                        db.session.add(m)
                        db.session.commit()
                        rows.remove(row)
