from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, Email, EqualTo

from trycars.ext.database.database import db
from trycars.ext.database.models import *
from .validations import exclusive_check, password_check, email_exists


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), exclusive_check()])
    email = EmailField('email', validators=[DataRequired(), Email(check_deliverability=True, message='Not a valid e-mail address.'), exclusive_check()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm_password', message='Password and confirmation must match'), password_check()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    recaptcha = RecaptchaField()


class EmailConfirmationForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), email_exists()])
    recaptcha = RecaptchaField()
