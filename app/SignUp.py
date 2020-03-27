# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
from app import app
from flask import render_template
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
ch.setLevel(logging.DEBUG)

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
BASE_PATH = "smart-card/"
BASE_URL = "http://192.168.0.193:5000/"
#BASE_URL = "localhost:5000/"
#BASE_URL = "http://d3446b58.ngrok.io/"
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

"""
Returns the UUID of the server
path : <address>/ping
"""
@app.route("/server-status")
def getServerStatus():
    return SERVER_STATUS

"""
Create a URL route in the application for "/"
Implementation only for web applications
Not implemented at the moment
TODO : implement web app
"""
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    """
    welcomeString = " Test URL"
    res = make_response(welcomeString,200)
    return res

@app.route("/smart-card/getImage/<photoID>")
def get_image(photoID):
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
    

@app.route("/smart-card/profile/<profileID>")
def getProfile(profileID):
    API_KEY_DB = getApiKeysFromDb()
    custDataDict = API_KEY_DB[profileID]
    encodingKey = custDataDict["encodingKey"]
    
    logger.info("Encoding Key:" + str(encodingKey))
    userProfiles = getUserProfiles()
    if userProfiles != -1:
        
        requestedProfile = userProfiles[encodingKey]
        profilePicture = BASE_URL + "smart-card/getImage/"+ requestedProfile["ProfilePhotoID"]
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

