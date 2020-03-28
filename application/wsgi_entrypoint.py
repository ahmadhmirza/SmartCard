#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:52:56 2020

@author: ahmad
"""

"""
Application's entry point
"""

from application import create_app

def main():
	app = create_app()
	app.run(host="0.0.0.0", debug = True)

if __name__ == "__main__":
	main()
    