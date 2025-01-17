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

        # Open file with newly added medication
        try:
            df_delta = pd.read_xml(
                delta_file, encoding='utf-8', xpath='meds/med')
            df_delta.fillna('', inplace=True)
        except ValueError:
            return None

        # Open file with drug register
        df_products = pd.read_json(file, encoding='utf-8-sig')
        df_products.fillna('', inplace=True)

        # Loop through newly added medication and write necessary information in database
        for product_delta in df_delta.itertuples():
            if product_delta[1] == (df_products.loc[df_products['authorisation_no'] ==
                                                    product_delta[1]].iloc[0]['authorisation_no']):
                name = product_delta[2]
                reg_number = product_delta[1]
                atc_code = df_products.loc[df_products['authorisation_no'] ==
                                           product_delta[1]].iloc[0]['atc_code']
                form = df_products.loc[df_products['authorisation_no'] ==
                                       product_delta[1]].iloc[0]['pharmaceutical_form_lv']
                active_substance = df_products.loc[df_products['authorisation_no'] ==
                                                   product_delta[1]].iloc[0]['active_substance']
                m = AddedMedication(
                    name=name,
                    regNumber=reg_number,
                    atcCode=atc_code,
                    form=form,
                    activeSubstance=active_substance)
                db.session.add(m)
                db.session.commit()

    @staticmethod
    def write_information(file_name):
        '''Function to write information to .csv file'''
        new_file_name = date.today().strftime('%Y%m%d') + '_' + file_name
        shutil.copyfile(file_name, new_file_name)
        with open(date.today().strftime('%Y%m%d') + '.csv', 'w', encoding='utf-8', newline='') as f:
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
                date.today().strftime('%Y%m%d') + '.csv')
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
    def insert_medication(file, doping_file, search_term):
        '''Function to create new products in database'''
        SearchedMedication.query.delete()  # Start with an empty table to avoid duplicates
        db.session.commit()

        # Open file with drug register
        df_products = pd.read_json(file, encoding='utf-8-sig')
        df_products.fillna('', inplace=True)

        # Search the drug register for entries matchin the search term
        df_searched = df_products[
            (df_products['atc_code'].str.contains(search_term)) |
            (df_products['active_substance'].str.contains(search_term, case=False)) |
            (df_products['authorisation_no'].str.contains(search_term))
        ].drop_duplicates(subset=['authorisation_no'])
        df_searched.fillna('', inplace=True)

        # Open file with information on use in sports
        df_doping = pd.read_csv(doping_file)
        df_doping.fillna('', inplace=True)

        # Write information for the searched medication
        for search_result in df_searched.itertuples():
            name = search_result[3]  # product.findtext('medicine_name')
            # product.findtext('authorisation_no')
            reg_number = search_result[5]
            atc_code = search_result[33]  # product.findtext('atc_code')
            # product.findtext('pharmaceutical_form_lv')
            form = search_result[15]
            # product.findtext('active_substance')
            active_substance = search_result[17]

            # If searched medication already has information about use in sports, include it
            if not df_doping.loc[df_doping['authorisation_no'] == search_result[5]].empty:
                include = False
                user_checked = True
                doping = True
                prohibited_out = df_doping.loc[df_doping['authorisation_no']
                                               == search_result[5]].iloc[0]['Aizliegts ārpus sacensībām']
                prohibited_in = df_doping.loc[df_doping['authorisation_no']
                                              == search_result[5]].iloc[0]['Aizliegts sacensību laikā']
                prohibited_class = df_doping.loc[df_doping['authorisation_no'] ==
                                                 search_result[5]].iloc[0]['Aizliegto vielu un metožu saraksta klase']
                notes = df_doping.loc[df_doping['authorisation_no'] ==
                                      search_result[5]].iloc[0]['Piezīmes par lietošanu']
                sports_in_competition_lv = df_doping.loc[df_doping['authorisation_no'] ==
                                                         search_result[5]].iloc[0]['Sporta veidi, kuros aizliegts sacensību laikā']
                sports_out_competition_lv = df_doping.loc[df_doping['authorisation_no'] ==
                                                          search_result[5]].iloc[0]['Sporta veidi, kuros aizliegts ārpus sacensībām']
                notes_en = df_doping.loc[df_doping['authorisation_no']
                                         == search_result[5]].iloc[0]['Notes']
                sports_in_competition_en = df_doping.loc[df_doping['authorisation_no'] ==
                                                         search_result[5]].iloc[0]['Prohibited In-Competition in the following sports']
                sports_out_competition_en = df_doping.loc[df_doping['authorisation_no'] ==
                                                          search_result[5]].iloc[0]['Prohibited Out-of-Competition in the following sports']

                m = SearchedMedication(name=name,
                                       regNumber=reg_number,
                                       atcCode=atc_code,
                                       form=form,
                                       activeSubstance=active_substance,
                                       include=include,
                                       userChecked=user_checked,
                                       doping=doping,
                                       prohibitedOUTCompetition=prohibited_out,
                                       prohibitedINCompetition=prohibited_in,
                                       prohibitedClass=prohibited_class,
                                       notesLV=notes,
                                       sportsINCompetitionLV=sports_in_competition_lv,
                                       sportsOUTCompetitionLV=sports_out_competition_lv,
                                       notesEN=notes_en,
                                       sportsINCompetitionEN=sports_in_competition_en,
                                       sportsOUTCompetitionEN=sports_out_competition_en,)
                db.session.add(m)
                db.session.commit()

            # Else write nothing in the table
            else:
                m = SearchedMedication(name=name,
                                       regNumber=reg_number,
                                       atcCode=atc_code,
                                       form=form,
                                       activeSubstance=active_substance)
                db.session.add(m)
                db.session.commit()

    @staticmethod
    def write_information(file_name):
        '''Function to write information to .csv file'''
        new_file_name = date.today().strftime('%Y%m%d') + '_' + file_name
        shutil.copyfile(file_name, new_file_name)
        with open(date.today().strftime('%Y%m%d') + '.csv', 'w', encoding='utf-8', newline='') as f:
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
                date.today().strftime('%Y%m%d') + '.csv')
            f.writelines(input_lines)
        df = pd.read_csv(new_file_name)
        df = df.drop_duplicates(subset=['authorisation_no'], keep='last')
        df.to_csv(new_file_name, index=False)


class NotesFields(db.Model):
    '''Model for database with notes about information on medications' use in sports'''
    __tablename__ = 'notes_fields'
    id = db.Column(db.Integer, primary_key=True)
    uniqueIdentifier = db.Column(db.Text, unique=True)
    atcCode = db.Column(db.String(10))
    form = db.Column(db.Text)
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
        '''Function to update the databases'''
        # Open drug register
        df_products = pd.read_json(drug_register, encoding='utf-8-sig')
        df_products.drop_duplicates(
            subset=['authorisation_no'], ignore_index=True, inplace=True)

        # Open file with information about medication use in sports
        df_doping = pd.read_csv(doping_register)
        df_doping.drop(columns=[
                       'medicine_name', 'active_substance'], inplace=True)

        # Create dataframe for information for Notes table
        df_products_columns = ['authorisation_no', 'atc_code']
        df_notes = df_products.drop(
            columns=[col for col in df_products if col not in df_products_columns])
        df_notes = df_notes.join(df_doping.set_index(
            'authorisation_no'), on='authorisation_no')
        df_notes.drop(columns=['authorisation_no'], inplace=True)
        df_notes.drop_duplicates(
            subset=['atc_code', 'pharmaceutical_form_lv'], ignore_index=True, inplace=True)

        df_notes.dropna(subset=['Aizliegts ārpus sacensībām', 'Aizliegts sacensību laikā'],
                        axis='index',
                        inplace=True,
                        ignore_index=True)
        df_notes.fillna('', inplace=True)

        # Write information from dataframe to database
        for note in df_notes.itertuples():
            if NotesFields.query.filter_by(uniqueIdentifier=f'{note[1]}_{note[2]}').first():
                continue
            m = NotesFields(uniqueIdentifier=f'{note[1]}_{note[2]}',
                            atcCode=note[1],
                            form=note[2],
                            prohibitedOUTCompetition=note[3],
                            prohibitedINCompetition=note[4],
                            prohibitedClass=note[5],
                            notesLV=note[6],
                            sportsINCompetitionLV=note[7],
                            sportsOUTCompetitionLV=note[8],
                            notesEN=note[9],
                            sportsINCompetitionEN=note[10],
                            sportsOUTCompetitionEN=note[11])
            db.session.add(m)
            db.session.commit()

    @staticmethod
    def rewrite_notes(drug_register, doping_register):
        '''Delete all records from notes_fields table'''
        NotesFields.query.delete()
        db.session.commit()
        NotesFields.update_notes(drug_register, doping_register)
