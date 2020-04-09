# models.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains db models for tables in
# the db in order to take advantage
# of flask_sqlalchemy

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id=admin_id).first()


class Racer(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    height = db.Column(
        db.Float,
        nullable=False
    )

    weight = db.Column(
        db.Float,
        nullable=False
    )

    reporter_id = db.Column(
        db.Integer
    )

    def __init__(self, name, height, weight, reporter_id):
        self.name = name
        self.height = height
        self.weight = weight
        self.reporter_id = reporter_id

    def __repr__(self):
        return f'Racer: {self.name}'


class Reporter(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Reporter: {self.name}'


class Race(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    number = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
    )

    date = db.Column(
        db.DateTime,
        nullable=False
    )

    cup = db.Column(
        db.String(80)
    )

    def __init__(self, number, date, cup):
        self.number = number
        self.date = date
        self.cup = cup

    def __repr__(self):
        return f'Race {self.number} - {self.cup}'


class Result(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    race_id = db.Column(
        db.Integer
    )

    racer_id = db.Column(
        db.Integer
    )

    def __init__(self, race_id, racer_id):
        self.race_id = race_id
        self.racer_id = racer_id

    def __repr__(self):
        return f'Race ID: {self.race_id}  Racer ID: {self.racer_id}'


class Admin(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String,
        nullable=False
    )

    name = db.Column(
        db.String(30),
        nullable=True
    )

    created_date = db.Column(
        db.DateTime,
        nullable=False
    )

    def __init__(self, username, password, name=False):
        from datetime import datetime
        from .extensions import encrypt

        self.username = username
        self.password = encrypt(password)

        if name:
            self.name = name

        self.created_date = datetime.now()

    def __repr__(self):
        return f'Admin: {self.username}'

    def is_authenticated(self):
        '''
        Returns True always as a logged-in user is always authenticated
        '''
        return True

    def is_active(self):
        '''
        Returns True always as active/inactive functionality isn't implemented
        '''
        return True

    def is_anonymous(self):
        '''
        Returns True always as anonymous functionality isn't implemented
        '''
        return True

    def get_id(self):
        '''
        Returns id of admin
        '''
        return self.id


class Email(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first = db.Column(
        db.String(80),
        nullable=False
    )

    last = db.Column(
        db.String(80),
        nullable=True
    )

    address = db.Column(
        db.String(80),
        nullable=False,
        unique=True
    )

    def __init__(self, first, address, last=False):
        self.first = first
        self.address = address
        self.last = last

    def __repr__(self):
        return f'Email: {self.address}'
