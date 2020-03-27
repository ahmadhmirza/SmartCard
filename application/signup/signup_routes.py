# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
from app import app
from flask import render_template,url_for
from flask import request,redirect,make_response
from werkzeug.utils import secure_filename
import uuid
import os
import json
###############################################################################

""" 
Initialization of all the necessary paths required for the script to run.
"""
from app import SC_constants as CONSTANTS
# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
TMP_PATH            = CONSTANTS.TMP_DIR
PROFILE_PHOTO_PATH  = CONSTANTS.PROFILE_PHOTO_DIR
apiDB_json          = CONSTANTS.API_DB_JSON
UsersDB_json        = CONSTANTS.USER_DB_JSON
# Storage directories for different file types.
sslCertificate      = CONSTANTS.SSL_CERTIFICATE
sslKey              = CONSTANTS.SSL_KEY

SERVER_ERROR_STRING = "The cookie monster is loose at out HQ and we are trying to get him under control, please give us a moment and try again later."

################################ Init Databases ##############################
def getApiKeysFromDb():
    API_KEY_DB={}
    try:
        with open(apiDB_json,"r") as apiDb_jsonFile:
            API_KEY_DB=json.load(apiDb_jsonFile)
        return API_KEY_DB
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        return -1
    
def getUserProfiles():
    try:
        with open(UsersDB_json,"r") as userProfiles_json:
            USER_PROFILES=json.load(userProfiles_json)
        return USER_PROFILES
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        return -1    
    
###############################################################################


    
################################ END OF SCRIPT ################################ 

