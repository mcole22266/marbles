# extensions.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains helper functions to assist
# all areas of the app while maintaining
# clean code.

from os import environ


def init_db(db, testdata=False, admin=False, commit=False):
    '''
    Initialize database.

    Args:
        db (SQLAlchemy): flask_sqlalchemy db object
        testdata (bool): Set True to initialize db with test data
        admin (bool): Set True to initialize db with temp admin(s)
        commit (bool): Set True for auto-commit
    '''

    if testdata:
        init_db_testdata(db, commit=commit)

    if admin:
        init_db_admin(db, commit=commit)

    if commit:
        db.session.commit()


def init_db_admin(db, commit=False):
    '''
    Initializes the database with temporary admin(s)

    Args:
        db (SQLAlchemy): flask_sqlalchemy db object
        commit (bool): Set True for auto-commit
    '''
    from .models import Admin

    admin = Admin('admin', 'adminpass')
    present = Admin.query.filter_by(username=admin.username).first()
    if not present:
        db.session.add(admin)

    if commit:
        db.session.commit()


def init_db_testdata(db, commit=False):
    '''
    Initializes the database with testdata until real data
    can be included.

    Args:
        db (SQLAlchemy): Flask database object created in models.py
        commit (Boolean): If true, function will commit throughout

    Returns:
        None
    '''
    from .db_connector import addSeries

    from .models import Racer, Race, Reporter, Result
    from datetime import date, timedelta
    from random import choice

    reporterNames = ['Jeff Jeffington', 'Geoff Geoffington',
                     'Mike Mikington', 'Michael Michaelton']
    for reporterName in reporterNames:
        present = Reporter.query.filter_by(name=reporterName).first()
        if not present:
            reporter = Reporter(reporterName)
            db.session.add(reporter)
    if commit:
        db.session.commit()

    racerTuples = [
        ('Black Jack', 16, 44, Reporter.query.filter_by(
            name='Jeff Jeffington').first()),
        ('Green Goblin', 16, 44, Reporter.query.filter_by(
            name='Geoff Geoffington').first()),
        ('White Lightning', 16, 44, Reporter.query.filter_by(
            name='Mike Mikington').first()),
        ('Blue Gooze', 16, 44, Reporter.query.filter_by(
            name='Michael Michaelton').first()),
    ]

    for racerTuple in racerTuples:
        name, ht, wt, reporter = racerTuple
        present = Racer.query.filter_by(name=name).first()
        if not present:
            racer = Racer(name, ht, wt, reporter.id)
            db.session.add(racer)
    if commit:
        db.session.commit()

    addSeries(db, 'Kynzi Cup', is_active=True, commit=True)

    startDate = date(2020, 3, 28)
    date = startDate
    for raceNum in range(1, 10):
        present = Race.query.filter_by(number=raceNum).first()
        if not present:
            race = Race(raceNum, date, 1)
            date += timedelta(days=1)
            db.session.add(race)
    if commit:
        db.session.commit()

    racers = Racer.query.all()
    races = Race.query.all()

    for race in races:
        winner = choice(racers)
        result = Result(race.id, winner.id, 1)
        db.session.add(result)
    if commit:
        db.session.commit()


def encrypt(string):
    '''
    Encrypts a given string

    Args:
        string (str): String to encrypt

    Returns:
        str: Encrypted string
    '''
    import hashlib

    hashed = hashlib.sha512(string.encode()).hexdigest()
    return hashed


def sendEmails(email, subject, content):
    '''
    Support function specifically to send email alerts
    to all email addresses available in the database.

    Args:
        subject (str): Subject of the Email
        content (str): Content of the Email

    Returns:
        None
    '''
    import yagmail
    GMAIL_USERNAME = environ['GMAIL_USERNAME']
    GMAIL_PASSWORD = environ['GMAIL_PASSWORD']

    yag = yagmail.SMTP(GMAIL_USERNAME, GMAIL_PASSWORD)

    content = f'Hey {email.first}!\n\n' + content

    yag.send(email.address, subject, content)
