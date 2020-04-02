# -*- coding: utf-8 -*-
"""
Created on Wed, April 01 10:10:10 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""

from flask_wtf import FlaskForm, RecaptchaField

# Field types can be imported from wtforms
# Field validators from wtforms.validators
from wtforms import StringField,TextField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Length, Optional

class SignupForm(FlaskForm):
    """ Form for new user registration"""
    lName = StringField("Last Name", [
        DataRequired(message=('*Last name cannot be empty.'))
        ])
    fName = StringField("First Name", [
        DataRequired(message=('*First name cannot be empty.'))
        ])
    password = StringField("Password", [
        DataRequired(message=('*Password cannot be empty.')),
        Length(min=4, message = ("Password must have atleast 4 characters."))
        ])
    catchPhrase = TextField("Catch Phrase (optional)", [Optional])
    #recaptcha = RecaptchaField()
    submit = SubmitField("Submit")