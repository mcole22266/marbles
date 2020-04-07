# config.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Python representation of environment variables
# to be used within the app. If a new enviornment
# variable is added in an env file, it likely needs
# to also be added here to be used by Flask.

from os import environ, urandom


class Config:
    '''
    Python representation of environment variables
    to be used within the app. If a new environment
    variable is added in an env file, it likely needs
    to also be added here to be used by Flask.
    '''

    # flask settings
    SECRET_KEY = urandom(32)
    FLASK_APP = environ['FLASK_APP']
    FLASK_ENV = environ['FLASK_ENV']
    FLASK_DEBUG = environ['FLASK_DEBUG']
    FLASK_HOST = environ['FLASK_HOST']
    FLASK_PORT = environ['FLASK_PORT']

