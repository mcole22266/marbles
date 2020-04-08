# __init__.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# App initialization

from flask import Flask, render_template

from .db_connector import getTotalWins
from .models import db

from.extensions import init_db_testdata


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

        init_db_testdata(db, commit=True)

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
        def admin():
            '''
            Routes user to the admin page of the app.

            Returns:
                render_template('admin.html')
            '''

            return render_template('admin.html',
                                   title='Admin - Marble Racing')

        @app.route('/sign-in', methods=['GET', 'POST'])
        def admin_signin():
            '''
            Routes user to the admin sign-in page of the app.

            Returns:
                render_template('admin_signin.html')
            '''

            return render_template('admin_signin.html',
                                   title='Sign-In - Marble Racing')

        return app
