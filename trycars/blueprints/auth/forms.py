from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import re
from password_strength import PasswordStats

from trycars.ext.database.database import db
from trycars.ext.database.models import *


def exclusive_check():
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
        if 8 > len(password) > 30:
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
        elif re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            error = 'Password must have at least one symbol'
        # strengh
        elif PasswordStats(password).strength() < 0.3:
            error = 'Password is to weak.'
        
        if error is not None:
            raise ValidationError(error)
    
    return _password_check


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), exclusive_check()])
    email = EmailField('email', validators=[DataRequired(), Email(check_deliverability=True, message='Not a valid e-mail address.'), exclusive_check()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm_password', message='Password and confirmation must match'), password_check()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
