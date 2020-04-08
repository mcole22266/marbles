# extensions.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains helper functions to assist
# all areas of the app while maintaining
# clean code.


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

    from .models import Racer, Race, Reporter, Result
    from datetime import datetime, timedelta
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

    startDate = datetime(2020, 3, 28)
    date = startDate
    for raceNum in range(1, 10):
        present = Race.query.filter_by(number=raceNum).first()
        if not present:
            race = Race(raceNum, date, 'Marble Cup')
            date += timedelta(days=1)
            db.session.add(race)
    if commit:
        db.session.commit()

    racers = Racer.query.all()
    races = Race.query.all()

    for race in races:
        winner = choice(racers)
        for racer in racers:
            if racer == winner:
                result = Result(race.id, racer.id, True)
            else:
                result = Result(race.id, racer.id, False)
            db.session.add(result)
    if commit:
        db.session.commit()
