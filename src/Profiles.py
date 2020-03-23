# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
import json
from flask import make_response
import logging

############ Logger Init##############
try:
    with open('Profiles_Log', 'w'):
        pass
except:
    pass

#Create Logger
logger = logging.getLogger("Profiles_Log")
logger.setLevel(logging.DEBUG)

#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#create file handler and set level to info
fh = logging.FileHandler(filename='Profiles_Log')
fh.setLevel(logging.DEBUG)


# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %I:%M:%S %p')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)

""" 
Initialization of all the necessary paths required for the script to run.
"""
import SC_constants as CONSTANTS
# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
TMP_PATH            = CONSTANTS.TMP_DIR
apiDB_json          = CONSTANTS.API_DB_JSON
UsersDB_json        = CONSTANTS.USER_DB_JSON
# Storage directories for different file types.
sslCertificate      = CONSTANTS.SSL_CERTIFICATE
sslKey              = CONSTANTS.SSL_KEY

#########################READ IN THE API_Keys db###############################
def getApiKeysFromDb():
    API_KEY_DB={}
    try:
        with open(apiDB_json,"r") as apiDb_jsonFile:
            API_KEY_DB=json.load(apiDb_jsonFile)
        return API_KEY_DB
    except Exception as e:
        print(str(e))
        logger.error(str(e))
        print("Unable to read API_Keys_db.json")
        return -1

def getUserProfiles():
    try:
        with open(UsersDB_json,"r") as userProfiles_json:
            USER_PROFILES=json.load(userProfiles_json)
        return USER_PROFILES
    except:
        print("Unable to read " + str(CONSTANTS.USERS_DB_JSON_FILENAME))
        return -1    
"""
apikeyInfoFunc
authenticates the apiKey passed in the request.
Passes user value directly to the function configured with the endpoint.
param : accessID : apiKey
    required_scopes
returns: user corresponding to the apiKey.
""" 
def basic_auth(accessID, required_scopes):
    API_KEY_DB = getApiKeysFromDb()
    
    if API_KEY_DB != -1:
        if accessID in API_KEY_DB.keys():
            custDataDict = API_KEY_DB[accessID]
            print("Requesting user ID'd as: " + custDataDict["lastName"])
            logger.info("Requesting user ID'd as: " + custDataDict["lastName"])
            return {'sub': "test"}
    else:
        print("Invalid AccessID, request denied.")
        logger.error("Invalid AccessID, request denied.")
        return None
    
def getProfile(profileID):
    API_KEY_DB = getApiKeysFromDb()
    custDataDict = API_KEY_DB[profileID]
    encodingKey = custDataDict["encodingKey"]
    logger.info("Encoding Key:" + str(encodingKey))
    userProfiles = getUserProfiles()
    if userProfiles != -1:
        
        requestedProfile = userProfiles[encodingKey]
        res = make_response(requestedProfile)
        return res
    else:
        print("Error(s) encountered in executing the service.")
        logger.error("Error(s) encountered in executing the service.")
        httpCode = 500
        res = make_response("Error(s) encountered in executing the service.",httpCode)
        return res
    

