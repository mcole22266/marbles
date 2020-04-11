# forms.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains form fields in order to take advantage
# of flask_wtf form handling

from os import environ

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (IntegerField, PasswordField, RadioField, StringField,
                     SubmitField, TextAreaField)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from .db_connector import getLastRace, getRacer
from .extensions import encrypt

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


def usernameExists_validation(form, field):
    '''
    Custom validator to ensure the user doesn't choose an already
    chosen username when signing up as an admin.
    '''
    from .db_connector import getAdmin
    username = form.username.data
    present = getAdmin(username=username)
    if present:
        raise ValidationError('This username is already in use')


def secret_code_validation(form, field):
    '''
    Custom validator to ensure new admins are verified by
    anyone who knows the secret code.
    '''
    encrypted_user_secret_code = encrypt(form.secret_code.data)
    encrypted_secret_code = environ['ENCRYPTED_SECRET_CODE']
    if encrypted_user_secret_code != encrypted_secret_code:
        raise ValidationError('The Secret Code is incorrect.')


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
    ])

    submit = SubmitField("Sign-In")


class SignUpForm(FlaskForm):
    '''
    Admin Sign-Up Form
    '''

    username = StringField('Username', [
        DataRequired(),
        usernameExists_validation
    ])

    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', 'Passwords must match')
    ])

    confirm = PasswordField('Confirm Password', [
        DataRequired()
    ])

    name = StringField('Name', render_kw={
        'placeholder': 'Optional'
    })

    secret_code = StringField('Secret Code', [
        DataRequired(),
        secret_code_validation
    ])

    submit = SubmitField('Sign-Up')


class EmailAlertForm(FlaskForm):
    '''
    Email Alerts sign-up form
    '''

    first = StringField('First Name', [
        DataRequired()
    ])

    last = StringField('Last Name', render_kw={
        'placeholder': 'Optional'
    })

    email = EmailField('Email', [
        DataRequired()
    ])

    submit = SubmitField('Sign-Up')


class sendEmailForm(FlaskForm):
    '''
    Form to send email to subscribers
    '''

    subject = StringField('Subject', [
        DataRequired()
    ])

    content = TextAreaField('Content', [
        DataRequired()
    ], render_kw={
        "rows": 10
    })

    submit = SubmitField('Send Emails')


class updateRaceDataForm(FlaskForm):
    '''
    Form to update race data
    '''

    race_number = IntegerField('Race Number', [
        DataRequired()
    ])

    cup = StringField('Series', [
        DataRequired()
    ])

    date = DateField('Date', [
        DataRequired()
    ])

    winner = RadioField('Winner', coerce=int)

    submit = SubmitField("Update")

    def __init__(self):
        super(updateRaceDataForm, self).__init__()
        self.winner.choices = [
            (racer.id, racer.name) for racer in getRacer(all=True)
        ]
        self.race_number.data = getLastRace() + 1


class activateSeriesForm(FlaskForm):
    '''
    Form to choose which series to make active
    '''

    series = StringField('Series To Activate', [
        DataRequired()
    ])

    submit = SubmitField('Activate')


class toggleActiveRacerForm(FlaskForm):
    '''
    Form to toggle active/inactive for racer
    '''

    racer = StringField('Racer', [
        DataRequired()
    ])

    submit = SubmitField('Toggle Racer')


class addRacerForm(FlaskForm):
    '''
    Form to add a new racer
    '''

    name = StringField('Name', [
        DataRequired()
    ])

    height = StringField('Height (mm)', [
        DataRequired()
    ])

    weight = StringField('Weight (oz)', [
        DataRequired()
    ])

    submit = SubmitField('Add Racer')


class contactForm(FlaskForm):
    '''
    Form to contact the site owners
    '''

    email = EmailField('Email Address', [
        DataRequired()
    ])

    content = TextAreaField('Ask us a question or beg us to release merch', [
        DataRequired()
    ], render_kw={
        "rows": 10
    })

    submit = SubmitField('Send')
