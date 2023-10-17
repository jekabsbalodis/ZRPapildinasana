import xml.etree.ElementTree as ET
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from . import db, login_manager


class Permission:
    WRITE = 1
    ADMIN = 2


class Role(db.Model):
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
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
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
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
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
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
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
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token, expiration=3600):
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
    def insert_medication(deltaFile, file):
        AddedMedication.query.delete()  # Start with an empty table to avoid duplicates
        db.session.commit()
        with open(deltaFile, encoding='utf-8') as df:
            allStuffDelta = ET.parse(df)
        productsDelta = allStuffDelta.findall('meds/med')
        with open(file, encoding='utf-8') as f:
            allStuff = ET.parse(f)
        products = allStuff.findall('products/product')
        productsDeltaChecked = []
        for productDelta in productsDelta:
            for product in products:
                if productDelta.findtext('reg_number') in productsDeltaChecked:
                    continue
                if productDelta.findtext('reg_number') == product.findtext('authorisation_no'):
                    name = productDelta.findtext('med_name')
                    regNumber = productDelta.findtext('reg_number')
                    atcCode = product.findtext('atc_code')
                    form = product.findtext('pharmaceutical_form_lv')
                    activeSubstance = product.findtext('active_substance')
                    m = AddedMedication(
                        name=name, regNumber=regNumber, atcCode=atcCode, form=form, activeSubstance=activeSubstance)
                    db.session.add(m)
                    db.session.commit()
                    productsDeltaChecked.append(
                        productDelta.findtext('reg_number'))

    def check_new_medication(submittedFile, regNumber):
        with open(submittedFile, 'rt') as file:
            reader = csv.reader(file, dialect='excel', delimiter=',')
            for row in reader:
                for field in row:
                    if field == regNumber:
                        return (True)


class NotesFields(db.Model):
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
    def update_notes(drugRegister, dopingRegister):
        with open(drugRegister, encoding='utf-8') as dr:
            allStuff = ET.parse(dr)
        products = allStuff.findall('products/product')

        lineChecked = []
        atcCodeChecked = []

        with open(dopingRegister, encoding='utf-8', newline='') as dr:
            reader = csv.reader(dr, dialect='excel', delimiter=',')
            for line in reader:
                if line[1] == 'authorisation_no':
                    continue
                for product in products:
                    if line[1] in lineChecked:
                        continue
                    authorisationNo = product.findtext('authorisation_no')
                    if line[1] == authorisationNo:
                        atcCode = product.findtext('atc_code')
                        if atcCode in atcCodeChecked:
                            continue
                        prohibitedOUTCompetition = line[4]
                        prohibitedINCompetition = line[5]
                        prohibitedClass = line[6]
                        notesLV = line[7]
                        sportsINCompetitionLV = line[8]
                        sportsOUTCompetitionLV = line[9]
                        notesEN = line[10]
                        sportsINCompetitionEN = line[11]
                        sportsOUTCompetitionEN = line[12]
                        m = NotesFields(atcCode=atcCode,
                                        prohibitedOUTCompetition=prohibitedOUTCompetition,
                                        prohibitedINCompetition=prohibitedINCompetition,
                                        prohibitedClass=prohibitedClass,
                                        notesLV=notesLV,
                                        sportsINCompetitionLV=sportsINCompetitionLV,
                                        sportsOUTCompetitionLV=sportsOUTCompetitionLV,
                                        notesEN=notesEN,
                                        sportsINCompetitionEN=sportsINCompetitionEN,
                                        sportsOUTCompetitionEN=sportsOUTCompetitionEN)
                        db.session.add(m)
                        db.session.commit()
                        lineChecked.append(line[1])
                        atcCodeChecked.append(atcCode)
