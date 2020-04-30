# extensions.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains helper functions to assist
# all areas of the app while maintaining
# clean code.


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
    from .db_connector import addAdmin

    addAdmin(db, 'admin', 'adminpass', 'Admin', commit=commit)


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

    from .models import Racer, Race, Result
    from datetime import date, timedelta
    from random import choice

    racerTuples = [
        ('Black Jack', 16, 44, 'rgb(25, 25, 25)'),
        ('Green Goblin', 16, 44, 'rgb(5, 99, 10)'),
        ('White Lightning', 16, 44, 'rgb(150, 150, 150)'),
        ('Blue Gooze', 16, 44, 'rgb(60, 50, 156)'),
    ]

    for racerTuple in racerTuples:
        name, ht, wt, color = racerTuple
        present = Racer.query.filter_by(name=name).first()
        if not present:
            racer = Racer(name, ht, wt, color)
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


def sendEmails(app, email, subject, content, greeting=True):
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
    GMAIL_USERNAME = app.config['GMAIL_USERNAME']
    GMAIL_PASSWORD = app.config['GMAIL_PASSWORD']

    yag = yagmail.SMTP(GMAIL_USERNAME, GMAIL_PASSWORD)

    if greeting:
        # only used for email alerts
        content = f'Hey {email.first}!\n\n' + content
        content += '\n\nWith deep love and gratitude,\nThe Marble Racers'
        yag.send(email.address, subject, content)

    else:
        # only used for contact form
        yag.send(email, subject, content)


def to_rgba(rgb, a):
    '''
    Converts rgb string to rgba string with a given alpha value.

    Args:
        rgb (str): rgb string to be converted
        a (float, int, str) = alpha value for new rgba

    Returns:
        String
    '''
    rgba = rgb.replace('rgb', 'rgba')
    rgba = f'{rgba[:-1]}, {a})'
    return rgba


def getEmbedded(url):
    '''
    Converts regular YouTube video URL into Embedded link.

    Args:
        url (str): The URL to convert into the embedded url

    Returns:
        String
    '''
    split_idx = url.find('=')
    id = url[split_idx+1:]
    embedded = f'https://www.youtube.com/embed/{id}'
    return embedded
