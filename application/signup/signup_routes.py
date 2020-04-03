# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
from flask import current_app as app
from flask import Blueprint, render_template,url_for
from flask import request,redirect,make_response
from werkzeug.utils import secure_filename
import uuid
import os
import logging
import json
############################# Logger Init#####################################
try:
    with open('WebServer.log', 'w'):
        pass
except:
    pass

#Create Logger
logger = logging.getLogger("WebServer_Log")
logger.setLevel(logging.DEBUG)

#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

#create file handler and set level to info
fh = logging.FileHandler(filename='WebServer.log')
fh.setLevel(logging.DEBUG)


# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %I:%M:%S %p')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)
###############################################################################

signup_bp = Blueprint('signup_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/signup')

""" 
Initialization of all the necessary paths required for the script to run.
"""
try:
    from application import SC_constants as CONSTANTS
    print("INFO: Signup: Imported configuration from package successfully.")
except:
    import SC_constants as CONSTANTS
    print("DEBUG: Signup: Running in Safe Mode: Imported alternative configuration.")
    
# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
PROFILE_PHOTO_PATH  = CONSTANTS.PROFILE_PHOTO_DIR
# Storage directories for different file types.
SERVER_ERROR_STRING = CONSTANTS.SERVER_ERROR_STRING
SUPPORTED_WEBSITES = CONSTANTS.SUPPORTED_WEBSITES
################################ Init Databases ##############################
try:
    from application import Data_Controller as dc 
    print("INFO: Signup: DB Controller initialized successfully.")
except:
    import Data_Controller as dc
    print("DEBUG: Signup: Safe Mode: Imported alternative DBC.")

API_KEY_DB      = dc.getApiKeysFromDb()
USER_PROFILES   = dc.getUserProfiles()


def isInitSuccessful():
    if API_KEY_DB == False:
        return False
    if USER_PROFILES == False:
        return False   
    return True
###############################################################################

def secureUpload():
    return True
"""
Create a URL route in the application for "/"
Implementation only for web applications
Not implemented at the moment
TODO : implement web app
"""

try:
    from application import forms
    print("INFO: Signup: Imported configuration from package successfully.")
except:
    import forms
    print("DEBUG: Signup: Running in Safe Mode: Imported alternative configuration.")
@signup_bp.route('/',methods=('GET', 'POST'))
def home():
    if isInitSuccessful():
        signupForm = forms.SignupForm()
        if request.method == 'POST':
            if signupForm.validate_on_submit():
                print("INFO: Signup: Form Data Validated.")
                print("INFO: Signup: new user registration, LastName: " + signupForm.lName.data)
                fName = signupForm.fName.data
                lName = signupForm.lName.data
                fullName = fName + " " + lName
                password = signupForm.password.data # TODO: Hash the password
                socialLinks = signupForm.socialLinks.data
                # 1- Generate a new API-key for the user.
                # API is generated for First and Last Name & user password.
                genApiKey = dc.addNewApiKey(fName,lName,password)

                #2- Save the profile photo and assign the photoID.
                try: # try to save the profile photo
                    #fileName = signupForm.profilePhoto.data.filename
                    #extension = fileName.rsplit(".",1)[1]
                    #TODO: verify allowed extension and file name.
                    #TODO: file size check
                    fileName = genApiKey # Save the uploaded file with the same name as the api key
                    signupForm.profilePhoto.data.save(os.path.join(PROFILE_PHOTO_PATH,fileName))
                    photoID = str(fileName)
                    print("Profile photo uploaded successfully.")
                except Exception as e:
                    print("ERROR: Signup: " + str(e))
                    print("ERROR: Signup: Placeholder profile photo will be used.")
                    photoID = "0"

                #3-Populate socialLinksDict from the form
                #TODO: Check for http/https in the provided URL
                socialLinks = socialLinks.split(",")
                socialLinksDict = {}
                for url in socialLinks:
                    for item in SUPPORTED_WEBSITES:
                        if item.lower() in url.lower():
                            socialLinksDict[item] = url
                        else:
                            pass
                ##################################################

                #4- Add User Profile to the database.
                accessKey = dc.addNewUserProfile(genApiKey,password,fullName, photoID, socialLinksDict)
                #3- Confirm user registration.
                #TODO: Send an automated email to admin-email with user registration details.
                print("INFO: Signup: New user registration successfull.")
                print("API-Key: " + str(genApiKey))
                
                #TODO: Page for successful registration.
                #TODO: Flash message implementation.
                newProfileURL = url_for('profiles_bp.getProfile',profileID=genApiKey)
                return redirect(newProfileURL)
                #return redirect(url_for('signup_bp.home'))
            else:
                print("ERROR: Signup: Form data validation failed.")
        return render_template("form.html",form = signupForm)
    else:
        welcomeString = "ERROR : INIT FAILED : SignUp "
        res = make_response(welcomeString,500)
        return res

################################ END OF SCRIPT ################################ 

