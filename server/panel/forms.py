from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class Config(FlaskForm):
    name = StringField('File Name', validators=[DataRequired()], default='stealer')
    os = SelectField('os', choices=['windows'])
    # chrome = BooleanField('Chrome')
    # brave = BooleanField('Brave')
    # chromium = BooleanField('Chromium')
    # opera = BooleanField('Opera')
    # amigo = BooleanField('Amigo')
    # firefox = BooleanField('Firefox')
    # edge = BooleanField('Microsoft Edge')
    submit = SubmitField('Create Build')


class Login(FlaskForm):
    login = StringField('User', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('log in')
