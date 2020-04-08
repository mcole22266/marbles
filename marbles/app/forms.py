# forms.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains form fields in order to take advantage
# of flask_wtf form handling

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

csrf = CSRFProtect()


class SignInForm(FlaskForm):
    '''
    Admin Sign-In Form
    '''

    username = StringField("Username", [
        DataRequired()
    ])

    password = PasswordField("Password", [
        DataRequired()
    ])

    submit = SubmitField("Sign-In")
