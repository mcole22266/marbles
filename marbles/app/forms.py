# forms.py
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Contains form fields in order to take advantage
# of flask_wtf form handling

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

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
