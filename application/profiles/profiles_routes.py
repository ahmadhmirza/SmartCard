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
                     url_prefix='/profiles')

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
@profiles_bp.route('/')
def home():
    if isInitSuccessful():
        welcomeString = " HOME PAGE: PROFILES"
        res = make_response(welcomeString,200)
        return res
    else:
        welcomeString = "ERROR: Profiles : INIT FAILED"
        res = make_response(welcomeString,500)
        return res


@profiles_bp.route("/getImage/<photoID>")
def getImage(photoID):
    defaultPlaceHolder = CONSTANTS.PLACEHOLDER_PHOTO_M
    #At signup if no profile photo is uploaded then default value will be 0
    if photoID != 0:
        #filename = photoID + ".jpg"
        filename = photoID
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
    if isInitSuccessful():
        API_KEY_DB      = dc.getApiKeysFromDb()
        if profileID in API_KEY_DB:
            #get the customer specific information from API_KEY_DB:
            custDataDict    = API_KEY_DB[profileID]
            #get the user's access key:
            accessKey     = custDataDict["accessKey"]
            logger.info("Access Key:" + str(accessKey))
            #Calculate the secret access key:
            accessKey = dc.generateSignature(profileID,accessKey)
            #Read the UsersDB_json
            userProfiles = dc.getUserProfiles()
            #Check if the read operation was successful.
            if userProfiles != False:
                #Get the user's profile from the database.
                requestedProfile = userProfiles[accessKey]
                profilePicture = url_for("profiles_bp.getImage",photoID=requestedProfile["ProfilePhotoID"])
                print("INFO: Profiles: Profile Photo URL: " + profilePicture)
                return render_template('UserProfile.html',
                                home_addr="localhost:5000/",
                                signin_addr= "localhost:5000/",
                                signup_addr= url_for("signup_bp.home"),
                                customerName=requestedProfile["Name"],
                                fb_addr = requestedProfile["FACEBOOK"],
                                linkdin_addr = requestedProfile["LINKEDIN"],
                                ig_addr = requestedProfile["INSTAGRAM"],
                                profile_photo = profilePicture)
            #IF the read operation on user profiles returned an error:
            else:
                print("Error(s) encountered in geting the user profiles database.")
                logger.error("Error(s) encountered in geting the user profiles database.")
                httpCode = 500
                res = make_response(SERVER_ERROR_STRING,httpCode)
                return res
        #profileID does not exist in the db
        else:
            MSG_STRING = "The requested profile does not exist in the user database."
            res = make_response(MSG_STRING,404)
            return res 
    #Init failed:
    else:
        ERROR_STRING = "ERROR: Profiles: INIT FAILED. "
        res = make_response(ERROR_STRING,500)
        return res 
################################ END OF SCRIPT ################################ 

