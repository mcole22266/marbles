# forms.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains form fields in order to take advantage
# of flask_wtf form handling

from os import environ

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from .db_connector import getLastRace, getRacer, getSeries, getVideo
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


def emailExists_validation(form, field):
    '''
    Custom validator to ensure multiple emails aren't added to the
    db when user's sign up.
    '''
    from .db_connector import getEmail
    email = form.email.data
    present = getEmail(address=email)
    if present:
        raise ValidationError('This Email is already in use')


def secret_code_validation(form, field):
    '''
    Custom validator to ensure new admins are verified by
    anyone who knows the secret code.
    '''
    encrypted_user_secret_code = encrypt(form.secret_code.data)
    encrypted_secret_code = environ['ENCRYPTED_SECRET_CODE']
    if encrypted_user_secret_code != encrypted_secret_code:
        raise ValidationError("Ah ah ah! You didn't say the magic word!")


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
        DataRequired(),
        emailExists_validation
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

    winner = SelectField('Winner', coerce=int)

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

    series = SelectField('Series To Activate', coerce=int)

    submit = SubmitField('Activate')

    def __init__(self):
        super(activateSeriesForm, self).__init__()
        self.series.choices = [
            (series.id, series.name) for series in getSeries(all=True)
        ]


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

    content = TextAreaField("Ask us a question or beg Tanner to shave \
        his 'stache", [
        DataRequired()
    ], render_kw={
        "rows": 10
    })

    submit = SubmitField('Send')


class seriesWinnerForm(FlaskForm):
    '''
    Form to set the series winner in the db
    '''
    series = SelectField('Series', coerce=int)

    winner = SelectField('Winner', coerce=int)

    submit = SubmitField('Update')

    def __init__(self):
        super(seriesWinnerForm, self).__init__()
        self.series.choices = [
            (series.id, series.name) for series in getSeries(all=True)
        ]
        self.winner.choices = [
            (racer.id, racer.name) for racer in getRacer(all=True)
        ]


class addVideoForm(FlaskForm):
    '''
    Form to add a new video
    '''

    url = StringField('URL', [
        DataRequired()
    ])

    groupname = StringField('Group', [
        DataRequired()
    ])

    name = StringField('Name', [
        DataRequired()
    ])

    description = TextAreaField('Description', [
        DataRequired()
    ], render_kw={
        "rows": 5
    })

    set_active = BooleanField('Set as Active')

    include_media = BooleanField('Include on Media Page')

    submit = SubmitField('Add Video')


class ManageVideoForm(FlaskForm):
    '''
    Form to choose which video to make active
    '''

    video = SelectField('Video To Activate', coerce=int)

    submit = SubmitField('Activate')
    delete = SubmitField('Delete')

    def __init__(self):
        super(ManageVideoForm, self).__init__()
        self.video.choices = [
            (video.id, f'{video.groupname} - {video.name}')
            for video in getVideo(all=True)
        ]
