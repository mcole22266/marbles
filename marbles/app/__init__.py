# __init__.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# App initialization

from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .db_connector import (addRace, addResult, getAdmin, getCups, getRace,
                           getRacer, getReporter, getResult, getTotalWins,
                           getUserFriendlyRacers, getUserFriendlyRaces,
                           verifyAdminAuth)
from .forms import SignInForm, csrf, updateRaceDataForm
from .models import db, login_manager

from.extensions import init_db, encrypt


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

            totalStandings = getTotalWins(db)
            names = []
            wins = []
            for result in totalStandings:
                names.append(result.name)
                wins.append(result.wins)

            return render_template('index.html',
                                   title='Marble Racing',
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

            if form.validate_on_submit():
                race_number = request.form.get('race_number')
                cup = request.form.get('cup')
                date = request.form.get('date')
                winner = request.form.get('winner')

                race = addRace(db, race_number, date, cup, commit=True)
                racer = getRacer(id=winner)
                addResult(db, race.id, racer.id, commit=True)

                return redirect(url_for('admin'))

            userFriendlyRacers = getUserFriendlyRacers(db)
            userFriendlyRaces = getUserFriendlyRaces(db)
            admins = getAdmin(all=True)
            races = getRace(all=True)
            racers = getRacer(all=True)
            reporters = getReporter(all=True)
            results = getResult(all=True)

            return render_template('admin.html',
                                   title='Admin - Marble Racing',
                                   form=form,
                                   cups=getCups(),
                                   userFriendlyRacers=userFriendlyRacers,
                                   userFriendlyRaces=userFriendlyRaces,
                                   admins=admins,
                                   races=races,
                                   racers=racers,
                                   reporters=reporters,
                                   results=results)

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
                                   title='Sign-In - Marble Racing',
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
                                   title='About - Marble Racing')

        @app.route('/info')
        def info():
            '''
            Routes a user to the Site Info page
            '''
            return render_template('info.html',
                                   title='Site Info - Marble Racing')

        @app.route('/data')
        def data():
            '''
            Routes a user to the Data Tables page
            '''
            userFriendlyRacers = getUserFriendlyRacers(db)
            userFriendlyRaces = getUserFriendlyRaces(db)
            admins = getAdmin(all=True)
            races = getRace(all=True)
            racers = getRacer(all=True)
            reporters = getReporter(all=True)
            results = getResult(all=True)
            return render_template('data.html',
                                   title='Data - Marble Racing',
                                   userFriendlyRacers=userFriendlyRacers,
                                   userFriendlyRaces=userFriendlyRaces,
                                   admins=admins,
                                   races=races,
                                   racers=racers,
                                   reporters=reporters,
                                   results=results)

        return app
