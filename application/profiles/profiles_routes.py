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

profiles_bp = Blueprint('profiles_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/dig-card/profiles')

""" 
Initialization of all the necessary paths required for the script to run.
"""
from application import SC_constants as CONSTANTS
# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
TMP_PATH            = CONSTANTS.TMP_DIR
PROFILE_PHOTO_PATH  = CONSTANTS.PROFILE_PHOTO_DIR
apiDB_json          = CONSTANTS.API_DB_JSON
UsersDB_json        = CONSTANTS.USER_DB_JSON
# Storage directories for different file types.
sslCertificate      = CONSTANTS.SSL_CERTIFICATE
sslKey              = CONSTANTS.SSL_KEY

SERVER_ERROR_STRING = CONSTANTS.SERVER_ERROR_STRING

################################ Init Databases ##############################
from application import Data_Controller as dc 

API_KEY_DB      = dc.getApiKeysFromDb
USER_PROFILES   = dc.getUserProfiles()

if API_KEY_DB == None:
    res = make_response (SERVER_ERROR_STRING,500)
    return res
if USER_PROFILES == None:
    res = make_response (SERVER_ERROR_STRING,500)
    return res
###############################################################################

"""
Create a URL route in the application for "/"
Implementation only for web applications
Not implemented at the moment
TODO : implement web app
"""
@profiles_bp.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    """
    welcomeString = " Test URL"
    res = make_response(welcomeString,200)
    return res

@profiles_bp.route("/getImage/<photoID>")
def getImage(photoID):
    defaultPlaceHolder = CONSTANTS.PLACEHOLDER_PHOTO_M
    #At signup if no profile photo is uploaded then default value will be 0
    if photoID != 0:
        filename = photoID + ".jpg"
        try:
            return send_from_directory(PROFILE_PHOTO_PATH,filename, mimetype='image/jpg')
        except Exception as e:
            print(str(e))
            logger.error(str(e))
            return send_from_directory(PROFILE_PHOTO_PATH,defaultPlaceHolder, mimetype='image/jpg')
    # no profile photo - return default placeholder.
    else:
        return send_from_directory(PROFILE_PHOTO_PATH,defaultPlaceHolder, mimetype='image/jpg')
    

@profiles_bp.route("/<profileID>")
def getProfile(profileID):
    API_KEY_DB = getApiKeysFromDb()
    custDataDict = API_KEY_DB[profileID]
    encodingKey = custDataDict["accessKey"]
    logger.info("Encoding Key:" + str(encodingKey))
    userProfiles = getUserProfiles()
    if userProfiles != -1:
        
        requestedProfile = userProfiles[encodingKey]
        profilePicture = url_for("profiles_bp.getImage",photoID=requestedProfile["ProfilePhotoID"])
        print(profilePicture)
        return render_template('UserProfile.html', 
                           customerName=requestedProfile["Name"],
                           fb_addr = requestedProfile["Facebook"],
                           linkdin_addr = requestedProfile["Linkedin"],
                           ig_addr = requestedProfile["Instagram"],
                           profile_photo = profilePicture)
    else:
        print("Error(s) encountered in executing the service.")
        logger.error("Error(s) encountered in executing the service.")
        httpCode = 500
        res = make_response(SERVER_ERROR_STRING,httpCode)
        return res
    

    
################################ END OF SCRIPT ################################ 

