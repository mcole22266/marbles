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
        return Racer.query.all()


def addRacer(db, name, height, weight, reporter_id, commit=False):
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
    racer = Racer(name, height, weight, reporter_id)
    db.session.add(racer)
    if commit:
        db.session.commit()

    return getRacer(name=name)


def getReporter(name=False, id=False):
    '''
    Return a Reporter object from the db if it exists

    Args:
        name (string): Pass name to get reporter by name
        id (int): Pass id to get reporter by id

    Returns:
        Reporter
    '''
    from .models import Reporter
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
    reporter = Reporter(name)
    db.session.add(reporter)
    if commit:
        db.session.commit()

    return getReporter(name=name)


def getRace(number=False, id=False):
    '''
    Return a Race object from the db if it exists

    Args:
        number (int): Pass name to get race by number
        id (int): Pass id to get race by id

    Returns:
        Race
    '''
    from .models import Race
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
    race = Race(number, date, cup)
    db.session.add(race)
    if commit:
        db.session.commit()

    return getRace(number=number)


def getResult(id=False, race_id=False, racer_id=False):
    '''
    Return a Result object from the db if it exists

    Args:
        id (int): Pass id to get result by id

    Returns:
        Result
    '''
    from .models import Result
    if id:
        return Result.query.filter_by(id=id).first()
    if race_id:
        return Result.query.filter_by(race_id=race_id).first()
    if racer_id:
        return Result.query.filter_by(racer_id=racer_id).first()


def addResult(db, race_id, racer_id, commit=False):
    '''
    Add a Result object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        race_id (int): Race id
        racer_id (int): Racer id
        commit (bool): Set True to commit changes
    Returns:
        Result
    '''
    from .models import Result
    result = Result(race_id, racer_id)
    db.session.add(result)
    if commit:
        db.session.commit()

    return getResult(race_id=race_id)


def getAdmin(username=False, name=False):
    '''
    Get an Admin by username or name.

    Args:
        username (str): Pass a username to get an admin by username
        name (str): Pass a name to get an admin by name

    Returns:
        Admin
    '''
    from .models import Admin

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

    admin = Admin(username, password, name=name)
    db.session.add(admin)

    if commit:
        db.session.commit()

    return admin


def getTotalWins(db):
    results = db.session.execute('''
SELECT
    racer.name AS name,
    COUNT(result.id) AS wins
FROM
    racer
LEFT JOIN
    result ON racer.id=result.racer_id
GROUP BY
    racer.name
ORDER BY
    racer.name;
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


def getCups():
    from .models import db
    results = db.session.execute('''
SELECT DISTINCT
    cup
FROM
    race;
''')
    return results
