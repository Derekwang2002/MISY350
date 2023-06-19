# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session
from jinja2  import TemplateNotFound

# App modules
from app import app, db
from app.models import Member, Tmatch, Challenge

# other modules
from datetime import datetime
from sqlalchemy import extract
import json

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenges_init', methods=['GET', 'POST'])
def challenges_init():
    currentMEID = '1' # session['loggedUser'] # get currently loggin user MEID
    members = Member.query.all()
    meids = db.session.query(Member.MEID).all()
    
    # get time info
    currentYear = datetime.now().year
    currentSeason = int(datetime.now().month/3 + 0.7)
    
    # forming label set (latest 5 seasons)
    chartLabel = []
    chartLabelData = []
    for i in range(1,currentSeason+1):
        chartLabelData.append(f'{currentYear} s{i}')
    for i in range(currentSeason,5):
        chartLabelData.append(f'{currentYear - 1} s{i}')
    
    # forming category (labels) for chart
    chartLabelData.sort()
    for  data in chartLabelData:
        chartLabel.append({'label': f'{data}'})
    chartLabel = json.dumps(chartLabel)
    
    # store MEIDs
    meidList = []
    for meid in meids:
        meidList.append(meid.MEID)
        
    # for each user, generate match data for chart
    memberMatches = {}
    for meid in meidList:
        winner_ym_dates = db.session.query(extract('year', Tmatch.DateOfMatch), extract('month', Tmatch.DateOfMatch)).filter(Tmatch.WinnerMEID==int(meid))
        loser_ym_dates = db.session.query(extract('year', Tmatch.DateOfMatch), extract('month', Tmatch.DateOfMatch)).filter(Tmatch.LoserMEID==int(meid))
        memberMatches[f'{meid}'] = [] # each member holds a list in super dict
        
        # ======== temporary variables ============
        Match = memberMatches[f'{meid}']
        winData = {k: 0 for k in chartLabelData}
        loseData = {k: 0 for k in chartLabelData}
        
        # for each win record, count them by their year+season 
        for winner_ym_date in winner_ym_dates:
            season = int(winner_ym_date[1]/3 + 0.7)
            year = winner_ym_date[0]
            
            if year == currentYear:
                winData[f'{currentYear} s{season}'] += 1
            elif year == currentYear - 1 and season >= currentSeason:
                winData[f'{currentYear - 1} s{season}'] += 1
                
        # for each lose record, count them by their year+season         
        for loser_ym_date in loser_ym_dates:
            season = int(loser_ym_date[1]/3 + 0.7)
            year = loser_ym_date[0]
            
            if loser_ym_date[0] == currentYear:
                loseData[f'{currentYear} s{season}']

                        
                    
        
        

    # new a challenge record
    if request.method == 'POST':
        cdate = datetime.now()
        cnote = request.form.get('challengeNote')
        cedid = request.form.get('challengedID')
        cerid = currentMEID
        
        # write challenge msg into database
        # add_challenge = Challenge(ChallengerMEID=cerid, ChallengedMEID=cedid, DateOfChallenge=cdate ,Notes=cnote)
        # db.session.add(add_challenge)
        # db.session.commit()
        # db.session.refresh(add_challenge)
        flash('Successfullyl sent request!')
        
        return render_template(
            'challenges_init.html', 
            members=members, chartLabel=chartLabel
            # cnote=cnote, cedid=cedid, cerid=cerid, cdate=cdate
        )
    
    return render_template(
        'challenges_init.html', 
        members=members, chartLabel=chartLabel
        # totalWin=totalWin, totalLose=totalLose
    )
            
            

@app.route('/challenges_sent')
def challenges_sent():
    session['meid'] = 1
    sentChallenges = db.session.query(Challenge).filter(Challenge.ChallengerMEID == session.get('meid'))
    
    return render_template('challenges_sent.html', sentChallenges=sentChallenges)

@app.route('/challenges_inbox')
def challenges_inbox():
    return render_template('challenges_inbox.html')

@app.route('/del')
def delete():
    cid = request.args.get('cid')
    deleted_challenge = Challenge.query.get(int(cid))
    db.session.delete(deleted_challenge)
    db.session.commit()
    sentChallenges = db.session.query(Challenge).filter(Challenge.ChallengerMEID == session.get('meid'))
    return render_template('challenges_sent.html', sentChallenges=sentChallenges)

@app.route('/t')
def test():
    current_time = datetime.now()
    return render_template('test.html', ct=current_time)