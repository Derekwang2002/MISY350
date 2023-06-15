# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash
from jinja2  import TemplateNotFound

# App modules
from app import app, db
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenges_init')
def challenges_init():
    return render_template('challenges_init.html')

@app.route('/challenges_sent')
def challenges_sent():
    return render_template('challenges_sent.html')
@app.route('/challenges_inbox')
def challenges_inbox():
    return render_template('challenges_inbox.html')
