# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	
    # Set up the App SECRET_KEY
    SECRET_KEY = 'S_U_perS3crEt_KEY#9999'

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
