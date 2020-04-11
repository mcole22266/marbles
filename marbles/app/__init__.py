# __init__.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# App initialization

from threading import Thread

from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .db_connector import (activateSeries, addEmail, addRace, addRacer,
                           addResult, addSeries, getAdmin, getEmail, getRace,
                           getRacer, getResult, getSeries, getTotalWins,
                           getUserFriendlyRacers, getUserFriendlyRaces,
                           getUserFriendlySeries, toggleRacer, verifyAdminAuth)
from .forms import (EmailAlertForm, SignInForm, activateSeriesForm,
                    addRacerForm, csrf, sendEmailForm, toggleActiveRacerForm,
                    updateRaceDataForm)
from .models import db, login_manager

from.extensions import init_db, encrypt, sendEmails, to_rgba


def create_app():
    '''
    Created a Flask App as per the App Factory Pattern

    Returns:
        Flask App
    '''

    app = Flask(__name__, instance_relative_config=False,
                template_folder='templates',
                static_folder='static')
    app.config.from_object('config.Config')

    with app.app_context():

        db.init_app(app)
        db.create_all()
        db.session.commit()

        init_db(db, testdata=True, admin=True, commit=True)

        login_manager.init_app(app)
        login_manager.login_view = 'admin_signin'
        csrf.init_app(app)

        @app.route('/', methods=['GET', 'POST'])
        def index():
            '''
            Routes user to the index page of the app.

            Returns:
                render_template('index.html')
            '''
            form = EmailAlertForm()

            if form.validate_on_submit():
                first = request.form.get('first')
                address = request.form.get('email')
                try:
                    last = request.form.get('last')
                except Exception:
                    last = False

                email = addEmail(db, first, address, last, commit=True)
                subject = "Alert Confirmation"
                content = "You've successfully been added to our contact list!\
                           \n\nThank you!\nThe Marble Racers"
                thread = Thread(target=sendEmails, args=[
                    email, subject, content])
                thread.start()

                return redirect(url_for('index'))

            racers = getRacer(active=True)
            activeSeries = getSeries(active=True)
            totalStandings = getTotalWins(db, activeSeries=activeSeries)
            names = []
            wins = []
            borderWidths = []
            for result in totalStandings:
                names.append(result.name)
                wins.append(result.wins)
                borderWidths.append(1.5)
            backgroundColors = []
            hoverColors = []
            borderColors = []
            for racer in racers:
                backgroundColors.append(to_rgba(racer.color, 0.4))
                hoverColors.append(to_rgba(racer.color, 0.7))
                borderColors.append(to_rgba(racer.color, 1))

            return render_template('index.html',
                                   title='The Marble Race',
                                   form=form,
                                   racers=racers,
                                   activeSeries=activeSeries.name,
                                   borderWidths=borderWidths,
                                   backgroundColors=backgroundColors,
                                   hoverColors=hoverColors,
                                   borderColors=borderColors,
                                   names=names,
                                   wins=wins)

        @app.route('/admin', methods=['GET', 'POST'])
        @login_required
        def admin():
            '''
            Routes user to the admin page of the app.

            Returns:
                render_template('admin.html')
            '''
            form = updateRaceDataForm()
            emailForm = sendEmailForm()
            seriesForm = activateSeriesForm()
            toggleRacerForm = toggleActiveRacerForm()
            racerForm = addRacerForm()

            try:
                subject = request.form['subject']
                content = request.form['content']
                formType = 'sendEmail'
            except Exception:
                try:
                    series = request.form['series']
                    formType = 'activateSeries'
                except Exception:
                    try:
                        racer = request.form['racer']
                        formType = 'toggleRacer'
                    except Exception:
                        try:
                            name = request.form['name']
                            height = request.form['height']
                            weight = request.form['weight']
                            color = request.form['color']
                            formType = 'addRacer'
                        except Exception:
                            formType = 'updateRaces'

            if formType == 'addRacer':
                # name, height, weight, color set in try block
                if racerForm.validate_on_submit():
                    addRacer(db, name, height, weight, color, commit=True)
                    return redirect(url_for('admin'))

            if formType == 'toggleRacer':
                if toggleRacerForm.validate_on_submit():
                    # racer already set in try block
                    toggleRacer(racer)
                    return redirect(url_for('admin'))

            if formType == 'activateSeries':
                if seriesForm.validate_on_submit():
                    # series already set in try block
                    addSeries(db, series, commit=True)
                    activateSeries(series)
                    return redirect(url_for('admin'))

            if formType == 'sendEmail':
                if emailForm.validate_on_submit():
                    # subject and content already set in try block
                    emails = getEmail(all=True)
                    for email in emails:
                        thread = Thread(target=sendEmails, args=[
                            email, subject, content])
                        thread.start()
                    return redirect(url_for('admin'))

            if formType == 'updateRaces':
                if form.validate_on_submit():
                    race_number = request.form.get('race_number')
                    cup = request.form.get('cup')
                    date = request.form.get('date')
                    winner = request.form.get('winner')

                    race = addRace(db, race_number, date, cup, commit=True)
                    racer = getRacer(id=winner)
                    series = getSeries(name=cup)
                    addResult(db, race.id, racer.id, series.id, commit=True)

                    return redirect(url_for('admin'))

            userFriendlyRacers = getUserFriendlyRacers(db)
            userFriendlyRaces = getUserFriendlyRaces(db)
            userFriendlySeries = getUserFriendlySeries(db)
            admins = getAdmin(all=True)
            races = getRace(all=True)
            racers = getRacer(all=True)
            results = getResult(all=True)
            emails = getEmail(all=True)
            serieses = getSeries(all=True)
            cups = [series.name for series in getSeries(all=True)]
            activeSeries = getSeries(active=True)

            return render_template('admin.html',
                                   title='Admin - The Marble Race',
                                   form=form,
                                   emailForm=emailForm,
                                   seriesForm=seriesForm,
                                   toggleRacerForm=toggleRacerForm,
                                   racerForm=racerForm,
                                   cups=cups,
                                   serieses=serieses,
                                   activeSeries=activeSeries,
                                   userFriendlyRacers=userFriendlyRacers,
                                   userFriendlyRaces=userFriendlyRaces,
                                   userFriendlySeries=userFriendlySeries,
                                   admins=admins,
                                   races=races,
                                   racers=racers,
                                   results=results,
                                   emails=emails)

        @app.route('/sign-in', methods=['GET', 'POST'])
        def admin_signin():
            '''
            Routes user to the admin sign-in page of the app.

            Returns:
                render_template('signin.html')
            '''
            form = SignInForm()

            if form.validate_on_submit():
                username = request.form.get('username')
                password = encrypt(request.form.get('password'))

                if verifyAdminAuth(username, password, encrypted=True):
                    admin = getAdmin(username)
                    login_user(admin)

                    next = request.args.get('next')
                    return redirect(next or url_for('admin'))

            return render_template('signin.html',
                                   title='Sign-In - The Marble Race',
                                   form=form)

        @app.route('/logout')
        @login_required
        def logout():
            '''
            Logs a logged-in user out before routing them to the admin
            sign-in page
            '''
            logout_user()
            return redirect(url_for('admin_signin'))

        @app.route('/about')
        def about():
            '''
            Routes a user to the About page
            '''
            return render_template('about.html',
                                   title='About - The Marble Race')

        @app.route('/info')
        def info():
            '''
            Routes a user to the Site Info page
            '''
            return render_template('info.html',
                                   title='Site Info - The Marble Race')

        @app.route('/data')
        def data():
            '''
            Routes a user to the Data Tables page
            '''
            userFriendlyRacers = getUserFriendlyRacers(db)
            userFriendlyRaces = getUserFriendlyRaces(db)
            userFriendlySeries = getUserFriendlySeries(db)
            admins = getAdmin(all=True)
            races = getRace(all=True)
            racers = getRacer(all=True)
            results = getResult(all=True)
            emails = getEmail(all=True)
            return render_template('data.html',
                                   title='Data - The Marble Race',
                                   userFriendlyRacers=userFriendlyRacers,
                                   userFriendlyRaces=userFriendlyRaces,
                                   userFriendlySeries=userFriendlySeries,
                                   admins=admins,
                                   races=races,
                                   racers=racers,
                                   results=results,
                                   emails=emails)

        return app
