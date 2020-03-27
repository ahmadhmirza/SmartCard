# -*- coding: utf-8 -*-
"""
Created on Mon, March 23 13:13:13 2020
@author: Ahmad H. Mirza
scriptVersion = 1.0..0
"""
import os

DATABASE_DIR_NAME       = "Database"
TMP_DIR_NAME            = "tmp"
PROFILE_PHOTO_DIR_NAME  = "ProfilePictures"
SSL_CERT_DIR_NAME       = "OpenSSLCertificate"
API_DB_JSON_FILENAME    = "API_Keys_db.json"
USERS_DB_JSON_FILENAME  = "Profiles.json"

PLACEHOLDER_PHOTO_M     = "placeholder_m.png"
SCRIPT_PATH = os.path.dirname(__file__)

DB_DIR      = os.path.join(SCRIPT_PATH,DATABASE_DIR_NAME)
TMP_DIR     = os.path.join(DB_DIR,TMP_DIR_NAME)
CERT_DIR    = os.path.join(DB_DIR,SSL_CERT_DIR_NAME)
############################################################
API_DB_JSON     = os.path.join(DB_DIR,API_DB_JSON_FILENAME)
USER_DB_JSON    = os.path.join(DB_DIR,USERS_DB_JSON_FILENAME)
PROFILE_PHOTO_DIR = os.path.join(DB_DIR,PROFILE_PHOTO_DIR_NAME)
#Directories for security certificates for HTTPs implementation
SSL_CERTIFICATE     = CERT_DIR+ "/cert.pem"
SSL_KEY             = CERT_DIR + "/key.pem"
############################################################




