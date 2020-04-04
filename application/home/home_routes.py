# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
from flask import current_app as app
from flask import Blueprint, render_template,url_for
from flask import request,redirect,make_response,send_from_directory
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

###############################################################################

home_bp = Blueprint('home_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/home')

""" 
Initialization of all the necessary paths required for the script to run.
"""
try:
    from application import SC_constants as CONSTANTS
    print("INFO: Profiles: Imported configuration from package successfully.")
except:
    import SC_constants as CONSTANTS
    print("DEBUG: Profiles: Running in Safe Mode: Imported alternative configuration.")
    
# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
PROFILE_PHOTO_PATH  = CONSTANTS.PROFILE_PHOTO_DIR
# Storage directories for different file types.
SERVER_ERROR_STRING = CONSTANTS.SERVER_ERROR_STRING

################################ Init Databases ##############################
try:
    from application import Data_Controller as dc 
    print("INFO: Profiles: DB Controller initialized successfully.")
except:
    import Data_Controller as dc
    print("DEBUG: Profiles: Safe Mode: Imported alternative DBC.")


API_KEY_DB      = dc.getApiKeysFromDb()
USER_PROFILES   = dc.getUserProfiles()

def isInitSuccessful():
    if API_KEY_DB == False:
        return False
    if USER_PROFILES == False:
        return False   
    return True
###############################################################################

"""
Create a URL route in the application for "/"
Implementation only for web applications
Not implemented at the moment
TODO : implement web app
"""
@home_bp.route('/')
def home():
    if isInitSuccessful():
        welcomeString = " HOME PAGE: PROFILES"
        res = make_response(welcomeString,200)
        return render_template("Home.html",
                                home_addr=url_for("home_bp.home"),
                                signin_addr= url_for("home_bp.home"),
                                signup_addr= url_for("signup_bp.home"))
    else:
        welcomeString = "ERROR: Profiles : INIT FAILED"
        res = make_response(welcomeString,500)
        return res

