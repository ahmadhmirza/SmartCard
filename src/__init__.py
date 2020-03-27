#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 08:46:51 2020

@author: ahmad
"""


"""
__init__.py file is considered a package, and can be imported. When you import 
a package, the __init__.py executes and defines what symbols the package 
exposes to the outside world.
"""

from flask import Flask

app = Flask(__name__)

from app import routes