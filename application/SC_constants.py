# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
import os

"""
Directory Names
"""
DATABASE_DIR_NAME       = "Database"
#Directories under DATABASE directory:
TMP_DIR_NAME            = "tmp"
PROFILE_PHOTO_DIR_NAME  = "ProfilePictures"
SSL_CERT_DIR_NAME       = "OpenSSLCertificate"
API_DB_JSON_FILENAME    = "API_Keys_db.json"
USERS_DB_JSON_FILENAME  = "Profiles.json"
##This is under PROFILE_PHOTO_DIR
PLACEHOLDER_PHOTO_M     = "placeholder_m.png"

"""
Paths
"""
#get the path to the current script:
#This will facilitate in geting the rest of the path programatically.
SCRIPT_PATH = os.path.dirname(__file__)

DB_DIR      = os.path.join(SCRIPT_PATH,DATABASE_DIR_NAME)
# TMP directory is not needed at the moment.
#TMP_DIR     = os.path.join(DB_DIR,TMP_DIR_NAME)
#CERT_DIR    = os.path.join(DB_DIR,SSL_CERT_DIR_NAME)
############################################################
API_DB_JSON     = os.path.join(DB_DIR,API_DB_JSON_FILENAME)
USER_DB_JSON    = os.path.join(DB_DIR,USERS_DB_JSON_FILENAME)
PROFILE_PHOTO_DIR = os.path.join(DB_DIR,PROFILE_PHOTO_DIR_NAME)
#Directories for security certificates for HTTPs implementation
#SSL_CERTIFICATE     = CERT_DIR+ "/cert.pem"
#SSL_KEY             = CERT_DIR + "/key.pem"
############################################################

SUPPORTED_WEBSITES =["FACEBOOK",
                     "INSTAGRAM",
                     "LINKEDIN"]
"""
Hard coded message strings go here.
"""
SERVER_ERROR_STRING = "The cookie monster is loose at out HQ and we are trying to get him under control, please give us a moment and try again later."



