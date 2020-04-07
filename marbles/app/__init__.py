# __init__.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# App initialization

from flask import Flask

def create_app():
    '''
    Created a Flask App as per the App Factory Pattern

    Args:
        None
    Returns:
        Flask App
    '''

    app = Flask(__name__, instance_relative_config=False,
                template_folder='templates',
                static_folder='static')
    app.config.from_object('config.Config')

    with app.app_context():

        @app.route('/', methods=['GET', 'POST'])
        def index():
            return 'Hello World'

        return app
