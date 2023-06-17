# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session
from jinja2  import TemplateNotFound

# App modules
from app import app, db
from app.models import Member

# other modules
from datetime import datetime

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenges_init', methods=['GET', 'POST'])
def challenges_init():
    if request.method == 'POST':
        members = Member.query.all()
        ctitle = request.form.get('challengeTitle')
        cnote = request.form.get('challengeNote')
        cedid = request.form.get('challengedID')
        cdate = datetime.now()
        cerid = ''
        # cerid = session['loggedUser']

        # write challenge msg into database
        return render_template(
            'challenges_init.html', 
            members=members, ctitle=ctitle, cnote=cnote, 
            cedid=cedid, cerid=cerid, cdate=cdate
        )
    
    return render_template('challenges_init.html')
            
            

@app.route('/challenges_sent')
def challenges_sent():
    return render_template('challenges_sent.html')

@app.route('/challenges_inbox')
def challenges_inbox():
    return render_template('challenges_inbox.html')

@app.route('/t')
def test():
    current_time = datetime.now()
    return render_template('test.html', ct=current_time)