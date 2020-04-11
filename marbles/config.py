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

    def convert_bool(str_bool):
        '''
        Used to convert string booleans into real booleans.
        NOTE: This function needs to be called for all boolean
        env variables
        '''
        if str_bool.lower() == 'false':
            return False
        else:
            return True

    # flask settings
    SECRET_KEY = urandom(32)
    FLASK_APP = environ['FLASK_APP']
    FLASK_ENV = environ['FLASK_ENV']
    FLASK_DEBUG = environ['FLASK_DEBUG']
    FLASK_HOST = environ['FLASK_HOST']
    FLASK_PORT = environ['FLASK_PORT']

    # postgres settings
    POSTGRES_USER = environ['POSTGRES_USER']
    POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
    POSTGRES_DB = environ['POSTGRES_DB']

    # sqlalchemy settings
    SQLALCHEMY_DATABASE_URI = environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = convert_bool(
        environ['SQLALCHEMY_TRACK_MODIFICATIONS'])

    # gmail settings
    GMAIL_USERNAME = environ['GMAIL_USERNAME']
    GMAIL_PASSWORD = environ['GMAIL_PASSWORD']

    # init settings
    INIT_TEST_DATA = convert_bool(environ['INIT_TEST_DATA'])
    INIT_ADMIN_DATA = convert_bool(environ['INIT_ADMIN_DATA'])
