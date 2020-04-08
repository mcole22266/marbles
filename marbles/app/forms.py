# forms.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains form fields in order to take advantage
# of flask_wtf form handling

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (IntegerField, PasswordField, RadioField, StringField,
                     SubmitField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError

from .db_connector import getLastRace, getRacer

csrf = CSRFProtect()


def admin_validation(form, field):
    '''
    Custom Validator for Admin Sign-In page
    '''
    from .db_connector import verifyAdminAuth
    username = form.username.data
    password = form.password.data
    if not verifyAdminAuth(username, password, encrypted=False):
        raise ValidationError('Incorrect username/password combo')


class SignInForm(FlaskForm):
    '''
    Admin Sign-In Form
    '''

    username = StringField("Username", [
        DataRequired(),
        admin_validation
    ])

    password = PasswordField("Password", [
        DataRequired(),
        admin_validation
    ])

    submit = SubmitField("Sign-In")


class updateRaceDataForm(FlaskForm):
    '''
    Form to update race data
    '''

    race_number = IntegerField('Race Number', [
        DataRequired()
    ])

    cup = StringField('Cup', [
        DataRequired()
    ])

    date = DateField('Date', [
        DataRequired()
    ])

    winner = RadioField('Winner')

    submit = SubmitField("Update")

    def __init__(self):
        super(updateRaceDataForm, self).__init__()
        self.winner.choices = [
            (racer.id, racer.name) for racer in getRacer(all=True)
        ]
        self.race_number.data = getLastRace()
