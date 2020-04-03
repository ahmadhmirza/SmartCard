# -*- coding: utf-8 -*-
"""
Created on Mon, March 30 10:10:10 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
import json
from datetime import datetime
import secrets
""" 
Initialization of all the necessary paths required for the script to run.
"""
try:
    from application import SC_constants as CONSTANTS
    print("Imported configuration from package successfully.")
except:
    import SC_constants as CONSTANTS
    print("Running in Safe Mode: Imported alternative configuration.")

# Storage directory for uploaded files.
DB_PATH             = CONSTANTS.DB_DIR
PROFILE_PHOTO_PATH  = CONSTANTS.PROFILE_PHOTO_DIR
API_KEY_DB_json     = CONSTANTS.API_DB_JSON
USERS_DB_json       = CONSTANTS.USER_DB_JSON

BYTESIZE = 16 # for generating Api Key string using secrets module
####################################################################

def writeJson(filePath,pyDictionary):
    try:
        with open(filePath,"w") as outFile:
            json.dump(pyDictionary, outFile, indent=4)
        return True
    except Exception as e:
        print(str(e))
        return False
    
def getTimeStamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def generateApiKey():
    apiKey = secrets.token_hex(BYTESIZE)
    return apiKey

"""
Function to generate signature from file and encoding key
"""
import hmac
from hashlib import md5    
def generateSignature(apiKey,encodingKey):
     #h = hashlib.md5()
    h = hmac.new(encodingKey.encode(),msg = None,digestmod=md5)
    h.update(apiKey.encode())
    signature= h.hexdigest()
    return signature

"""
Function to read API-Keys Database 
return: dictionary of the json file / False
"""
def getApiKeysFromDb():
    API_KEY_DB={}
    try:
        with open(API_KEY_DB_json,"r") as apiDb_jsonFile:
            API_KEY_DB=json.load(apiDb_jsonFile)
        return API_KEY_DB
    except Exception as e:
        print(str(e))
        #logger.error(str(e))
        return False
"""
Function to read User profile database
return: dictionary of user profiles / False
"""    
def getUserProfiles():
    try:
        with open(USERS_DB_json,"r") as userProfiles_json:
            USER_PROFILES=json.load(userProfiles_json)
        return USER_PROFILES
    except Exception as e:
        print(str(e))
        #logger.error(str(e))
        return False  
"""
Generate and add a new API key to the database.
Next step should be to add the user profile data to the
relevant db
return
"""   
def addNewApiKey(fName,lName, accessKey):
    #Read the DB containing API_Keys
    API_KEY_DB = getApiKeysFromDb()
    if API_KEY_DB != False: #If read operation is successful
        apiKey = generateApiKey()   # generate a new API key
        
        API_KEY_DB[apiKey] = {      # write new key to the read db
            "firstName"	    : fName,
            "lastName" 	    : lName,
            "accessKey"	    : accessKey,
            "timeStamp"	    : getTimeStamp()
            }
        
        if writeJson(API_KEY_DB_json,API_KEY_DB): # write operation successful?
            print("New API-Key generated successfully!")
            print(apiKey)
            print("-----------------------------------")
            return apiKey
        else:
            print("Error(s) encountered in API-Key generation.")
            return False
    else:
        print("Error(s) encountered in API-Key generation.")
        return False
 
"""
Generate and add new user data to the database.
return: True/false depending on the operation results.
"""         
def addNewUserProfile(apiKey, accessKey, name, photoId,socialLinksDict):
    # read the user database
    USER_PROFILES = getUserProfiles()
    if USER_PROFILES != False: # if read operation successful
        #generate a unique accessKey based on the apikey and the accesskey
        #given by the user.
        accessKey = generateSignature(apiKey,accessKey)
        USER_PROFILES[accessKey] = {
            "Name"	            : name,
            # TODO: "Sex"               : sex,
            "ProfilePhotoID"    : photoId,
            }
        
        for entry in socialLinksDict:
             USER_PROFILES[accessKey][entry] = socialLinksDict[entry]
         
        if writeJson(USERS_DB_json,USER_PROFILES): # write operation successful?
            print("New user's data added to db successfully")
            print("-----------------------------------")
            return accessKey
        else:
            print("Error(s) encountered in adding new user data.")
            return False
    else:
        print("Error(s) encountered in reading Users Database.")
        return False
 
    
"""
using main function for unit testing functions.
"""    
def unitTest():
    print("-----------------------------------")
    print("Performing unit tests:")
    print("Generate a new API key and User profile to database.")
    print("-----------------------------------")
    fName = "Johanna"
    lName = "Doe"
    fullName = fName +" "+lName
    accessKey = "1234"
    photoId = "6969420.jpg"
    socialLinksDict={
        "FACEBOOK":"https://www.facebook.com/",
        "INSTAGRAM":"https://www.instagram.com/",
        "LINKEDIN":"https://www.linkedin.com/"
        }
    
    key_api = addNewApiKey(fName,lName,accessKey)  
    key_usr = addNewUserProfile(key_api, accessKey, fullName, photoId, socialLinksDict)
    
    print("Test results: API_KEY:" + key_api)
    print("Test results: API_KEY:" + key_usr)
    API_DB = getApiKeysFromDb()
    USER_PROFILES = getUserProfiles()
    
    if key_api in API_DB:
        print("Test Case: Add new API-Key: Passed")
    else:
        print("Test Case: Add new API-Key: Failed")
    if key_usr in USER_PROFILES:
        print("Test Case: Add new user info: Passed")
    else:
        print("Test Case: Add new user info: Failed")
      
#if __name__ == "__main__":
#    unitTest()

