# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
from flask import render_template
from flask import request,redirect,make_response
from werkzeug.utils import secure_filename
import connexion
import uuid
import os
import logging
import json
############ Logger Init##############
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


# Create the application instance
app = connexion.App(__name__, specification_dir='./')


#Initialize server
SERVER_STATUS = {
        "Server_uuid" :  str(uuid.uuid4()),
        "ServerStatus": "Initializing...",
        "Message" : "Roses are red, violets are blue, unexpected } on line 32."
        
        }

# Dictionary containing the names of html files
### Front end / web-applications
HTML_TEMPLATES={
        "home"          : "UserProfile.html"
        }

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

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
    except Exception as e:
        print(str(e))
        return -1    
    
####################Configuration parameters for web server####################
# TODO : switch to app.config for flask
"""
#Commands for using app.config module.
app.config["IMAGE_UPLOADS"] = UPLOAD_IMG_PATH
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG","JPG","PNG"]
#Sets max filesize globally to 50MB
app.config["MAX_UPLOAD_FILE_SIZE"] = 50*1024*1024
"""
APP_CONFIG={
        #"IMAGE_UPLOADS":UPLOAD_IMG_PATH,
        "ALLOWED_IMAGE_EXTENSIONS":["JPEG","JPG","PNG"],
        "MAX_UPLOAD_FILE_SIZE" : 10*1024*1024 #10MB
        }
###############################################################################

logger.debug("WebServer with UUID %s started."%SERVER_STATUS["Server_uuid"])

"""
Returns the UUID of the server
path : <address>/ping
"""
@app.route("/serverStatus")
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
    :return:        the rendered template 'home.html'
    """
    res = {
        "Facebook": "https://www.facebook.com/ahmadhassan.mirza",
        "Instagram": "https://www.instagram.com/ahm_adhm/",
        "Linkedin": "https://www.linkedin.com/in/ahmad-hassan-mirza-50176946/",
        "Name": "Ahmad Hassan Mirza"
        }

    return render_template('UserProfile.html', 
                           customerName=res["Name"],
                           fb_addr = res["Facebook"],
                           linkdin_addr = res["Linkedin"],
                           ig_addr = res[""])

@app.route("/profile/<profileID>")
def getProfile(profileID):
    API_KEY_DB = getApiKeysFromDb()
    custDataDict = API_KEY_DB[profileID]
    encodingKey = custDataDict["encodingKey"]
    logger.info("Encoding Key:" + str(encodingKey))
    userProfiles = getUserProfiles()
    if userProfiles != -1:
        
        requestedProfile = userProfiles[encodingKey]
        #res = make_response(requestedProfile)

        return render_template('UserProfile.html', 
                           customerName=requestedProfile["Name"],
                           fb_addr = requestedProfile["Facebook"],
                           linkdin_addr = requestedProfile["Linkedin"],
                           ig_addr = requestedProfile["Instagram"])
    else:
        print("Error(s) encountered in executing the service.")
        logger.error("Error(s) encountered in executing the service.")
        httpCode = 500
        res = make_response("Error(s) encountered in executing the service.",httpCode)
        return res
    
"""
Runs the script.
The choice of which certificate to use can be configured here.
"""
if __name__ == '__main__':
    SERVER_STATUS["ServerStatus"] = "Running"
    #For using ad-hoc certificate generated from pyOpenSSL
    #app.run(host='0.0.0.0',port=5000,ssl_context='adhoc',debug=True)
    ##########################################################################
    app.run(host='192.168.0.193',port=5000,debug=True)
    #app.run(host='127.0.0.1',port=5000,debug=True)
    
################################ END OF SCRIPT ################################ 

