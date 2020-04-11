# db_connector.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Collection of helper functions used
# to more simply query or add items
# to the db


def getRacer(name=False, id=False, all=False):
    '''
    Return a Racer object from the db if it exists

    Args:
        name (string): Pass name to get racer by name
        id (int): Pass id to get racer by id
        all (bool): Pass True to return all Racers

    Returns:
        Racer
    '''
    from .models import Racer
    if name:
        return Racer.query.filter_by(name=name).first()
    if id:
        return Racer.query.filter_by(id=id).first()
    if all:
        return Racer.query.order_by((Racer.name.asc())).all()


def addRacer(db, name, height, weight, reporter_id,
             color, is_active=True, commit=False):
    '''
    Add a Racer object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        name (String): Racer name
        height (float): Racer's height
        weight (float): Racer's weight
        reporter_id (int): Racer's reporter id
        commit (bool): Set True to commit changes

    Returns:
        Racer
    '''
    from .models import Racer
    present = getRacer(name=name)
    if not present:
        racer = Racer(name, height, weight, reporter_id, color, is_active)
        db.session.add(racer)
        if commit:
            db.session.commit()

    return getRacer(name=name)


def getReporter(name=False, id=False, all=True):
    '''
    Return a Reporter object from the db if it exists

    Args:
        name (string): Pass name to get reporter by name
        id (int): Pass id to get reporter by id
        all (bool): Pass True to get all reporters

    Returns:
        Reporter
    '''
    from .models import Reporter
    if all:
        return Reporter.query.all()
    if name:
        return Reporter.query.filter_by(name=name).first()
    if id:
        return Reporter.query.filter_by(id=id).first()


def addReporter(db, name, commit=False):
    '''
    Add a Reporter object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        name (String): Reporter name
        commit (bool): Set True to commit changes
    Returns:
        Reporter
    '''
    from .models import Reporter
    present = getReporter(name=name)
    if not present:
        reporter = Reporter(name)
        db.session.add(reporter)
        if commit:
            db.session.commit()

    return getReporter(name=name)


def getRace(number=False, id=False, all=False):
    '''
    Return a Race object from the db if it exists

    Args:
        number (int): Pass name to get race by number
        id (int): Pass id to get race by id
        all (bool): Pass True to return all races

    Returns:
        Race
    '''
    from .models import Race
    if all:
        return Race.query.all()
    if number:
        return Race.query.filter_by(number=number).first()
    if id:
        return Race.query.filter_by(id=id).first()


def addRace(db, number, date, cup, commit=False):
    '''
    Add a Race object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        number (String): Race number
        date (datetime): Race date
        cup (string): Cup the race belongs to
        commit (bool): Set True to commit changes
    Returns:
        Race
    '''
    from .models import Race
    present = getRace(number=number)
    if not present:
        seriesPresent = getSeries(name=cup)
        if not seriesPresent:
            series = addSeries(db, name=cup, commit=True)
        else:
            series = seriesPresent
        race = Race(number, date, series.id)
        db.session.add(race)
        if commit:
            db.session.commit()

    return getRace(number=number)


def getSeries(name=False, active=False, id=False, all=False):
    '''
    Return a Series object from the db if it exists

    Args:
        name (int): Pass name to get series by name
        active (bool): Pass True to return only the current active series
        id (int): Pass id to get series by id
        all (bool): Pass True to return all series

    Returns:
        Series
    '''
    from .models import Series
    if all:
        return Series.query.all()
    if name:
        return Series.query.filter_by(name=name).first()
    if active:
        return Series.query.filter_by(is_active=active).first()
    if id:
        return Series.query.filter_by(id=id).first()


def addSeries(db, name, winner_id=False, is_active=False, commit=False):
    '''
    Add a Series object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        name (String): Series Name
        winner_id (str): Set Winner ID if there is an established winner
        is_active (bool): Set True if currently active
        commit (bool): Set True to commit changes
    Returns:
        Series
    '''
    from .models import Series
    present = getSeries(name=name)
    if not present:
        series = Series(name, winner_id, is_active)
        db.session.add(series)
        if commit:
            db.session.commit()

    return getSeries(name=name)


def getResult(id=False, race_id=False, racer_id=False, all=False):
    '''
    Return a Result object from the db if it exists

    Args:
        id (int): Pass id to get result by id

    Returns:
        Result
    '''
    from .models import Result
    if all:
        return Result.query.all()
    if id:
        return Result.query.filter_by(id=id).first()
    if race_id:
        return Result.query.filter_by(race_id=race_id).first()
    if racer_id:
        return Result.query.filter_by(racer_id=racer_id).first()


def addResult(db, race_id, racer_id, series_id, commit=False):
    '''
    Add a Result object to the db

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        race_id (int): Race id
        racer_id (int): Racer id
        commit (bool): Set True to commit changes
    Returns:
        Result
    '''
    from .models import Result
    result = Result(race_id, racer_id, series_id)
    db.session.add(result)
    if commit:
        db.session.commit()

    return getResult(race_id=race_id)


def getAdmin(username=False, name=False, all=False):
    '''
    Get an Admin by username or name.

    Args:
        username (str): Pass a username to get an admin by username
        name (str): Pass a name to get an admin by name
        all (bool): Pass True to return all admins

    Returns:
        Admin
    '''
    from .models import Admin

    if all:
        admins = Admin.query.all()
        return admins

    if username:
        admin = Admin.query.filter_by(username=username).first()

    if name:
        admin = Admin.query.filter_by(name=name).first()

    return admin


def addAdmin(db, username, password, name=False,
             encrypted=False, commit=False):
    '''
    Adds an admin user to the db.

    Args:
        db (SQLAlchemy): sqlalchemy db object
        username (str): Username for the admin
        password (str): Password for the admin
        name (str): optionally pass a name for the admin
        encyrpted (bool): Pass True if given password is encrypted
        commit (bool): Pass True to auto-commit the admin

    Returns:
        Admin
    '''
    from .models import Admin
    from .extensions import encrypt

    if not encrypted:
        password = encrypt(password)

    present = getAdmin(username=username)
    if not present:
        admin = Admin(username, password, name=name)
        db.session.add(admin)

        if commit:
            db.session.commit()

    return admin


def getEmail(address=False, id=False, all=False):
    '''
    Gets email from database

    Args:
        address (str): Get single email by address
        id (str): Get single email by id
        all (bool): Set True to return all emails in db

    Return:
        Email
    '''
    from .models import Email

    if all:
        return Email.query.all()
    if address:
        return Email.query.filter_by(address=address).first()
    if id:
        return Email.query.filter_by(id=id).first()


def addEmail(db, first, address, last=False, commit=False):
    '''
    Adds an email to the database

    Args:
        db (SQLAlchemy): db object
        first (str): First Name
        address (str): Email Address
        last (str): Last Name (optional)
        commit (bool): Set True to auto-commit
    Returns:
        Email
    '''
    from .models import Email

    present = getEmail(address=address)
    if not present:
        email = Email(first, address, last)
        db.session.add(email)
        if commit:
            db.session.commit()

    return getEmail(address=address)


def getTotalWins(db, activeSeries):
    results = db.session.execute(f'''
SELECT
    racer.name as name,
    SUM(CASE WHEN series.name='{activeSeries.name}' THEN 1 ELSE 0 END) AS wins
FROM
    racer
LEFT JOIN
    result ON result.racer_id=racer.id
LEFT JOIN
    series on result.series_id=series.id
GROUP BY
    racer.name
ORDER BY
    racer.name;
''')
    return results


def getUserFriendlyRaces(db):
    results = db.session.execute('''
SELECT
    race.number AS number,
    race.date AS date,
    racer.name AS winner,
    series.name AS series
FROM
    race
LEFT JOIN
    series ON race.series_id=series.id
LEFT JOIN
    result ON result.race_id=race.id
LEFT JOIN
    racer ON result.racer_id=racer.id;
''')
    return results


def getUserFriendlyRacers(db):
    results = db.session.execute('''
SELECT
    racer.name AS name,
    racer.height AS height,
    racer.weight AS weight,
    COUNT(result.racer_id) AS wins
FROM
    racer
LEFT JOIN
    result ON result.racer_id=racer.id
GROUP BY
    racer.name, racer.height, racer.weight
ORDER BY
    racer.name;
''')
    return results


def getUserFriendlySeries(db):
    results = db.session.execute('''
SELECT
    series.name AS name,
    racer.name AS winner
FROM
    series
LEFT JOIN
    racer ON racer.id=series.winner_id
ORDER BY
    series.id DESC;
''')
    return results


def verifyAdminAuth(username, password, encrypted=False):
    '''
    Verify the authentication of a given username/password

    Args:
        username (str): Username to authenticate
        password (str): Passowrd to authenticate
        encrypted (bool): Pass True is given password is encrypted

    Returns:
        bool - True if authenticated, False otherwise
    '''
    from .extensions import encrypt

    if not encrypted:
        password = encrypt(password)

    admin = getAdmin(username=username)

    if not admin:
        return False
    elif password != admin.password:
        return False
    else:
        return True


def getLastRace():
    from .models import db
    result = db.session.execute('''
SELECT
    MAX(number) AS last_race
FROM
    race;
''')
    return result.fetchone()[0]


def activateSeries(name):
    from .models import db
    db.session.execute(f'''
UPDATE
    series
SET
    is_active='f';
UPDATE
    series
SET
    is_active='t'
WHERE
    name='{name}';
''')
    db.session.commit()


def toggleRacer(name):
    from .models import db
    db.session.execute(f'''
UPDATE
    racer
SET
    is_active = NOT is_active
WHERE
    name='{name}';
''')
