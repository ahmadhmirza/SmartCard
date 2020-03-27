#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 08:46:51 2020

@author: ahmad

__init__.py file is considered a package, and can be imported. When you import 
a package, the __init__.py executes and defines what symbols the package 
exposes to the outside world.
"""


"""
command to run :
    flask run --host=0.0.0.0  # runs on internal network
    flask run  # runs on localhost
"""
from flask import Flask
import uuid


app = Flask(__name__)
from app import routes

#Initialize server
SERVER_STATUS = {
        "Server_uuid" :  str(uuid.uuid4()),
        "ServerStatus": "Initializing...",
        "Message" : "Roses are red, violets are blue, unexpected } on line 32."
        
        }