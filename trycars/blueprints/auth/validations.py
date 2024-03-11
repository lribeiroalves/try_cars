import re
from wtforms.validators import ValidationError
from password_strength import PasswordStats

from trycars.ext.database.database import db
from trycars.ext.database.models import *


def exclusive_check():
    """Username and Email exclusive validation for Registration Form"""
    def _exclusive_check(form, field):
        user = db.session.execute(db.select(User).filter_by(username=field.data)).scalar()
        if user is not None:
            raise ValidationError(f'Username "{field.data}" has already been taken.')
        
        user = db.session.execute(db.select(User).filter_by(email=field.data)).scalar()
        if user is not None:
            raise ValidationError(f'Email "{field.data}" has already been taken.')

    return _exclusive_check


def password_check():
    """
    Password Validation for Registration Form

    Verify the strength of 'password'
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        Has a strength score above 0.3 on password_strength.PasswordStats
    """

    def _password_check(form, field):
        password = field.data
        error = None
        # length
        if len(password) < 8 or len(password) > 30:
            error = 'Password must have between 8 and 30 characters.'
        # digits
        elif re.search(r"\d", password) is None:
            error = 'Password must have at least 1 digit.'
        # uppercase
        elif re.search(r"[A-Z]", password) is None:
            error = 'Password must have at least one uppercase letter'
        # lowercase
        elif re.search(r"[a-z]", password) is None:
            error = 'Password must have at least one lowercase letter'
        # symbols
        elif re.search(r"[ !#$@%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            error = 'Password must have at least one symbol'
        # strengh
        elif PasswordStats(password).strength() < 0.3:
            error = 'Password is to weak.'
        
        if error is not None:
            raise ValidationError(error)
    
    return _password_check


def email_exists():
    """Check if an email provided by the user exists in the database, this validation is used on EmailConfirmationForm"""

    def _email_exists(form, field):
        email = field.data

        user = db.session.execute(db.select(User).filter_by(email=email)).scalar()

        if user is None:
            raise ValidationError('Email not found.')
    
    return _email_exists


def user_exists():
    """Check if the login information provided by the user matches an existent user"""

    def _user_exists(form, field):
        login = field.data

        user = db.session.execute(db.select(User).filter_by(username=login)).scalar()
        

        if user is None:
            print(user)
            raise ValidationError('User not found.')
    
    return _user_exists