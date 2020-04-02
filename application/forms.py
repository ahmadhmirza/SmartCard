# -*- coding: utf-8 -*-
"""
Created on Wed, April 01 10:10:10 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""

from flask_wtf import FlaskForm, RecaptchaField
# Field types can be imported from wtforms
# Field validators from wtforms.validators
from wtforms import StringField,TextField,SubmitField,PasswordField,FileField
try:
    from wtforms.validators import DataRequired, Length, Optional,AnyOf
    print("imported validators.")
except:
    print("ROROEIJR")

class SignupForm(FlaskForm):
    
    """ Form for new user registration"""
    lName = StringField("Last Name",validators=[DataRequired()])
    fName = StringField("First Name")
    password = StringField("Password")
    catchPhrase = TextField("Catch Phrase (optional)")
    profilePhoto = FileField("Please select a Profile Photo")
    #recaptcha = RecaptchaField()
    submit = SubmitField("Submit")