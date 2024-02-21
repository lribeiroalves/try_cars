from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField
from wtforms.validators import DataRequired


class MyFirstForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])


class CaptchaForm(FlaskForm):
    user = StringField('user', validators=[DataRequired()])
    recaptcha = RecaptchaField()