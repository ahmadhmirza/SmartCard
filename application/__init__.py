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

"""initialize app"""
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    with app.app_context():
        from .profiles import profiles_routes
        app.register_blueprint(profiles_routes.profiles_bp)
        
        #TODO: register blue prints
        #Link https://hackersandslackers.com/flask-blueprints
        return app
