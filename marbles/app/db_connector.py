# db_connector.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Collection of helper functions used
# to more simply query or add items
# to the db


def getRacer(db, name=False, id=False):
    '''
    Return a Racer object from the db if it exists

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        name (string): Pass name to get racer by name
        id (int): Pass id to get racer by id

    Returns:
        Racer
    '''
    from .models import Racer
    if name:
        return Racer.query.filter_by(name=name).first()
    if id:
        return Racer.query.filter_by(id=id).first()


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
    '''
    from .models import Racer
    racer = Racer(name, height, weight, reporter_id)
    db.session.add(racer)
    if commit:
        db.session.commit()


def getReporter(db, name=False, id=False):
    '''
    Return a Reporter object from the db if it exists

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
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
    '''
    from .models import Reporter
    reporter = Reporter(name)
    db.session.add(reporter)
    if commit:
        db.session.commit()


def getRace(db, number=False, id=False):
    '''
    Return a Race object from the db if it exists

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
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
    '''
    from .models import Race
    race = Race(number, date, cup)
    db.session.add(race)
    if commit:
        db.session.commit()


def getResult(db, id=False):
    '''
    Return a Result object from the db if it exists

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        id (int): Pass id to get result by id

    Returns:
        Result
    '''
    from .models import Result
    if id:
        return Result.query.filter_by(id=id).first()


def addResult(db, race_id, racer_id, is_winner, commit=False):
    '''
    Add a Result object to the db if it doesn't exist.

    Args:
        db (SQLAlchemy): Flask sqlalchemy object
        race_id (int): Race id
        racer_id (int): Racer id
        is_winner (bool): True if given racer won the given race
        commit (bool): Set True to commit changes
    '''
    from .models import Result
    result = Result(race_id, racer_id, is_winner)
    db.session.add(result)
    if commit:
        db.session.commit()


def getTotalWins(db):
    results = db.session.execute('''
SELECT
    racer.name AS name,
    COUNT(result.is_winner) AS wins
FROM
    racer, result
WHERE
    racer.id=racer_id AND
    result.is_winner='t'
GROUP BY
    racer.name
ORDER BY
    racer.name;
''')
    return results
