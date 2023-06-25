# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session, jsonify
from jinja2  import TemplateNotFound

# App modules
from app import app, db
from app.models import member, tmatch, challenge, membership

# Other modules
import datetime
from sqlalchemy import extract, func
import json
from sqlalchemy.orm import aliased

# App main route + generic routing

# Structure: #
# ---------- #
# Home Page  #
# Challenge  #
# Member     #
# Match      #
# Membership #

# ============================================ Home Page (by Lv Wentian) ============================================= #
@app.route('/', methods=['POST', 'GET'])
def indexhome():
    # gender ratio
    members_num = member.query.count()
    member_f = member.query.filter(member.Gender == 'F').count()
    member_m = member.query.filter(member.Gender == 'M').count()
    f_ratio = (member_f/members_num)*100
    m_ratio = (member_m/members_num)*100
    gender_lay = [{'label': 'Female',
                   'value': f_ratio},
                  {'label': 'Male',
                   'value': m_ratio
                   }]
    gender_lay = json.dumps(gender_lay)

    # top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr = order_member[i].UTR
        mid = order_member[i].MEID
        utr_rank = {'label': str(mid), 'value': utr}
        l.append(utr_rank)
    l = json.dumps(l)
    # age group
    all_age = db.session.query(member.Age).all()
    age10 = []
    age20 = []
    age30 = []
    age40 = []
    age50 = []
    age60 = []
    age_group = []
    for i in all_age:
        if (i[0] > 10) & (i[0] < 20):
            age10.append(i)
            lb = '10+'
            age_group1 = {'label': lb, 'value': len(age10)}
        elif (i[0] >= 20) & (i[0] < 30):
            age20.append(i)
            lb = '20+'
            age_group2 = {'label': lb, 'value': len(age20)}
        elif (i[0] >= 30) & (i[0] < 40):
            age30.append(i)
            lb = '30+'
            age_group3 = {'label': lb, 'value': len(age30)}
        elif (i[0] >= 40) & (i[0] < 50):
            age40.append(i)
            lb = '40+'
            age_group4 = {'label': lb, 'value': len(age40)}
        elif (i[0] >= 50) & (i[0] < 60):
            age50.append(i)
            lb = '50+'
            age_group5 = {'label': lb, 'value': len(age50)}
        else:
            age60.append(i)
            lb = '60+'
            age_group6 = {'label': lb, 'value': len(age60)}
    age_group.append(age_group1)
    age_group.append(age_group2)
    age_group.append(age_group3)
    age_group.append(age_group4)
    age_group.append(age_group5)
    age_group.append(age_group6)
    age_group = json.dumps(age_group)

    createDate = db.session.query(member.DateOfCreation, (func.count(member.MEID))).group_by(member.DateOfCreation).all()
    list = []
    for i in createDate:
        dict = {'label': i[0], 'value': i[1]}
        list.append(dict)
    signup_num = json.dumps(list, cls=DateTimeEncoder)
        
    if request.method == 'POST':
        d_user = member.query.get(int(session.get('mid')))
        db.session.delete(d_user)
        db.session.commit()
    return render_template('index.html', chartdata1=gender_lay, data2=l, data3=age_group, data4=signup_num)


# ===================================================== CHALLENGE ===================================================== #
# ===================================================== by Wang Xingen ================================================ #
@app.route('/challengeLogin', methods=['GET', 'POST'])
def challengeLogin():
    return render_template('challenges_login.html')


@app.route('/challenges_board')
def challenges_board():
    currentMEID = session['mid']
    bulletinChallenges = db.session.query(challenge, member).\
        join(challenge, challenge.ChallengerMEID == member.MEID, isouter=True).\
        filter(challenge.IfBulletin == 1, challenge.Status == 0).all()
    return render_template('challenges_board.html', bulletinChallenges=bulletinChallenges, currentMEID=currentMEID) # challenges_board

@app.route('/challenges_init', methods=['GET', 'POST'])
def challenges_init():
    currentMEID = session['mid']
    members = member.query.all()
    meids = db.session.query(member.MEID).all()
    
    # =========== Chart info ===============
    # get time info
    currentYear = datetime.datetime.now().year
    currentSeason = int(datetime.datetime.now().month/3 + 0.7)
    
    # forming label set (latest 5 seasons)
    chartLabel = []
    chartLabelData = []
    for i in range(1,currentSeason+1):
        chartLabelData.append(f'{currentYear} S{i}')
    for i in range(currentSeason,5):
        chartLabelData.append(f'{currentYear - 1} S{i}')
    
    # forming category (labels) for chart
    chartLabelData.sort()
    for  data in chartLabelData:
        chartLabel.append({'label': f'{data}'})
    chartLabel = json.dumps(chartLabel)
    
    # store MEIDs
    meidList = []
    for meid in meids:
        meidList.append(meid.MEID)
        
    # for all user, store in dict
    memberMatches = {}
    # for each user, generate match data for chart: contains two list (win/lose - {value:num})
    for meid in meidList:
        # data for this member as winner/loser
        winner_ym_dates = db.session.query(
            extract('year', tmatch.DateOfMatch), extract('month', tmatch.DateOfMatch)).filter(tmatch.WinnerMEID==int(meid))
        loser_ym_dates = db.session.query(
            extract('year', tmatch.DateOfMatch), extract('month', tmatch.DateOfMatch)).filter(tmatch.LoserMEID==int(meid))
        
        # temporary variables 
        winData = {k: 0 for k in chartLabelData}
        loseData = {k: 0 for k in chartLabelData}
        
        # for each win record, count them by their year+season 
        for winner_ym_date in winner_ym_dates:
            season = int(winner_ym_date[1]/3 + 0.7)
            year = winner_ym_date[0]
            
            if year == currentYear:
                winData[f'{currentYear} S{season}'] += 1
            elif year == currentYear - 1 and season >= currentSeason:
                winData[f'{currentYear - 1} S{season}'] += 1
                
        # for each lose record, count them by their year+season         
        for loser_ym_date in loser_ym_dates:
            season = int(loser_ym_date[1]/3 + 0.7)
            year = loser_ym_date[0]
            
            if year == currentYear:
                loseData[f'{currentYear} S{season}'] += 1
            elif year == currentYear - 1 and season >= currentSeason:
                loseData[f'{currentYear - 1} S{season}'] += 1
    
        session[f'match-win-{meid}'] = json.dumps(
            [{'value':str(v)} for v in winData.values()]
        )
        session[f'match-lose-{meid}'] = json.dumps(
            [{'value':str(v)} for v in loseData.values()]
        )
    
    return render_template(
        'challenges_init.html', 
        members=members, chartLabel=chartLabel, memberMatches=memberMatches, 
        currentMEID=currentMEID
    )

# join table are required to present chellenged name and his/her UTR
@app.route('/challenges_sent')
def challenges_sent():
    currentMEID = session['mid']
    Challenge = aliased(challenge)
    Member = aliased(member)
    sentChallenges = db.session.query(Challenge, Member).\
        join(Member, Challenge.ChallengedMEID == Member.MEID, isouter=True).\
        filter(Challenge.ChallengerMEID == currentMEID).all()  # .options(joinedload(challenge.ChallengedMEID))
    sentCount = len(sentChallenges)
    return render_template('challenges_sent.html', sentChallenges=sentChallenges, sentCount=sentCount) # challenges_sent

@app.route('/challenges_inbox')
def challenges_inbox():
    currentMEID = session['mid']
    inChallenges = db.session.query(challenge, member).\
        join(member, challenge.ChallengerMEID == member.MEID, isouter=True).\
        filter(challenge.ChallengedMEID == currentMEID).all()
    return render_template('challenges_inbox.html', inChallenges=inChallenges)

@app.route('/challenges_settled')
def challenges_settled():
    currentMEID = session['mid']
    Tmatch = aliased(tmatch)
    Challenge = aliased(challenge)
    WinnerMember = aliased(member, name='winner_member')
    ChallengerMember = aliased(member, name='challenger_member')
    ChallengedMember = aliased(member, name='challenged_member')
    
    settledChallenges = db.session.query(Challenge, Tmatch, WinnerMember, ChallengerMember, ChallengedMember).\
        join(Tmatch, Challenge.CID == Tmatch.CID, isouter=True).\
        join(WinnerMember, Tmatch.WinnerMEID == WinnerMember.MEID, isouter=True).\
        join(ChallengerMember, Challenge.ChallengerMEID == ChallengerMember.MEID, isouter=True).\
        join(ChallengedMember, Challenge.ChallengedMEID == ChallengedMember.MEID, isouter=True).\
        filter(Challenge.Status == 2, 
               Challenge.ChallengedMEID==currentMEID or Challenge.ChallengerMEID==currentMEID).all()
    settledCount = len(settledChallenges)
    return render_template('challenges_settled.html', settledChallenges=settledChallenges, settledCount=settledCount) # challenges_settled

# ================== ajax route ===================== #
@app.route('/del', methods=['POST'])
def delete():
    cid = request.form.get('cid')
    deleted_challenge = challenge.query.get(int(cid))
    db.session.delete(deleted_challenge)
    db.session.commit()
    return f'successfully delete CID:{cid}'

@app.route('/change_status', methods=['POST'])
def change_status():
    status = request.json
    cid = int(status['cid'])
    status_change_challenge = challenge.query.get(cid)

    if status['status'] == 'accept':
        status_change_challenge.Status = 1
    elif status['status'] == 'reject':
        status_change_challenge.Status = -1
    
    result = {'message':'Success', 'status':status}
    db.session.commit()
    return result

@app.route('/change_status_new', methods=['POST'])
def change_status_new():
    currentMEID = session['mid']
    cid = request.form.get('cid')
    
    status_change_challenge = challenge.query.get(int(cid))
    status_change_challenge.Status = 1
    status_change_challenge.ChallengedMEID = currentMEID
    result = {'message':'Success'}
    db.session.commit()
    return result
    
    
@app.route('/init', methods=['POST'])
def init():
    cdate = datetime.datetime.now()
    cnote = request.form.get('challengeNote')
    cedid = request.form.get('challengedID')
    ifBulletin = request.form.get('ifBulletin')
    cerid = session['mid']
    
    # write challenge msg into database
    add_challenge = challenge(
        ChallengerMEID=cerid, ChallengedMEID=cedid, 
        DateOfChallenge=cdate ,Notes=cnote, Status=0, 
        IfBulletin=ifBulletin
    )
    db.session.add(add_challenge)
    db.session.commit()
    db.session.refresh(add_challenge)
    flash('Successfullyl sent request!')
    return f'Successfullyl sent request! {cedid} '

@app.route('/search', methods=['POST'])
def search():
    searchQuery = request.form.get('searchQuery')
    page = request.form.get('page')
    return f'{searchQuery} at {page}'


# ======================================================= Member ====================================================== #
# ======================================================= by Lv Wentian =============================================== #
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('new_register.html')

@app.route('/signup', methods=['GET', 'POST'])
def successfullsignup():
    # get input value
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    email = request.form.get('email')
    pword = request.form.get('password')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    age = request.form.get('age')
    utr = request.form.get('utr')
    # error checking
    error = False
    if len(pword) <= 8:
        flash('Please enter a password more than 8 words.')
        error = True
    # if phone.isdigit() == False:
    #     flash('Please enter the phone number with a correct format.')
    #     error = True
    if int(age) < 0:
        flash('Age must be greater than 0.')
        error = True
    if float(utr) > 16.5 or float(utr) < 1:
        flash('The UTR is between 1 and 16.5.')
        error = True
    if not error:
        user = ''
        user = member(FirstName=fname, LastName=lname, Email=email, MPassword=pword, Gender=gender,
                      Phone=phone, Age=age, UTR=utr, DateOfCreation=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return render_template('aftersignup.html', newuser=user)

    return render_template('new_register.html', password=pword, phone=phone, age=age, utr=utr, gender=gender,
                           firstname=fname, lastname=lname, email=email)

@app.route('/login')
def login():
    return render_template('new_login.html')

@app.route('/userhome')
def userhome():
    currentHour = datetime.datetime.now().hour
    greeting = ''
    if currentHour < 12:
        greeting = 'Good morning!'
    else:
        greeting = 'Good afternoon!'
    session['now'] = datetime.date.today()
    
    # top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr = order_member[i].UTR
        mid = order_member[i].MEID
        utr_rank = {'label': str(mid), 'value': utr}
        l.append(utr_rank)
    l = json.dumps(l)
    #matches held today
    matches_today=tmatch.query.filter(tmatch.DateOfMatch==datetime.date.today())
    #member's match
    winmatch_num=tmatch.query.filter(tmatch.WinnerMEID==session['mid']).count()
    losematch_num=tmatch.query.filter(tmatch.LoserMEID==session['mid']).count()
    return render_template(
        'userhome.html', message=greeting, data2=l,
        match_info=matches_today, winnum=winmatch_num, losenum=losematch_num
    )

@app.route('/userhomepage', methods=['GET', 'POST'])
def informationSubmit():
    # get input
    username = request.form.get('mid')
    pword = request.form.get('password')
    # valid check
    userinfo = member.query.get(username)  # this users whole info
    existing_mid = db.session.query(member.MEID).all()
    existing_mid = [x[0] for x in existing_mid]
    if int(username) in existing_mid:
        if username == '26' and pword == '123456789':
            createDate = db.session.query(member.DateOfCreation, (func.count(member.MEID))).group_by(member.DateOfCreation).all()
            list = []
            for i in createDate:
                dict = {'label': i[0], 'value': i[1]}
                list.append(dict)
                data = json.dumps(list, cls=DateTimeEncoder)
            return render_template('dashboard.html', data=data)
        if pword == userinfo.MPassword:
            session['mid'] = username  # MEID
            session['name'] = member.query.get(session['mid']).FirstName
            session['lname'] = member.query.get(session['mid']).LastName
            session['email'] = member.query.get(session['mid']).Email
            session['phone'] = member.query.get(session['mid']).Phone
            session['age'] = member.query.get(session['mid']).Age
            session['pword'] = member.query.get(session['mid']).MPassword
            session['gender'] = member.query.get(session['mid']).Gender
            session['utr'] = member.query.get(session['mid']).UTR
            currentHour = datetime.datetime.now().hour
            greeting = ''
            if currentHour < 12:
                greeting = 'Good morning!'
            else:
                greeting = 'Good afternoon!'
            # top utr members
            order_member = member.query.order_by((member.UTR).desc()).all()
            l = []
            for i in range(10):
                # for i in order_member:
                utr = order_member[i].UTR
                mid = order_member[i].MEID
                utr_rank = {'label': str(mid), 'value': utr}
                l.append(utr_rank)
            l = json.dumps(l)
            #matches held today
            matches_today=tmatch.query.filter(tmatch.DateOfMatch==datetime.date.today())
            #member's match
            winmatch_num=tmatch.query.filter(tmatch.WinnerMEID==session['mid']).count()
            losematch_num=tmatch.query.filter(tmatch.LoserMEID==session['mid']).count()
            return render_template(
                'userhome.html', message=greeting, data2=l, 
                match_info=matches_today, winnum=winmatch_num, losenum=losematch_num
            )
        else:
            flash("Error! The password and user does not match! Please try again.")
    else:
        flash('This member dose not exist, please try again!')
    # error checking
    return render_template('new_login.html')

@app.route('/accountsetting')
def account():
    return render_template('account.html')

@app.route('/accountmodify', methods=['GET', 'POST'])
def accountchange():
    # get input
    fname = request.form.get('firstName')
    lname = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phoneNumber')
    gender = request.form.get('gender')
    age = request.form.get('age')
    pword = request.form.get('password')
    # error checking
    error = False
    if len(pword) <= 8:
        flash('Please enter a password more than 8 words.')
        error = True
    if phone.isdigit() == False:
        flash('Please enter the phone number with a correct format.')
        error = True
    if int(age) < 0:
        flash('Age must be greater than 0.')
        error = True
    if not error:
        existing_user = member.query.get(session['mid'])
        existing_user.FirstName = fname
        existing_user.LastName = lname
        existing_user.Email = email
        existing_user.Phone = phone
        existing_user.Gender = gender
        existing_user.Age = age
        existing_user.MPassword = pword
        existing_user.verified = True
        db.session.commit()
        session['name'] = fname
        session['lname'] = lname
        session['email'] = email
        session['phone'] = phone
        session['age'] = age
        session['pword'] = pword
        session['gender'] = gender
        flash('Your information has been updated successfully!')
    return render_template('account.html')

@app.route('/accountdelete')
def aboutdelete():
    return render_template('accountdelete.html')



# ======================================================= Match ======================================================= #
# ======================================================= by Luo Jinghua ============================================== #
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
    
@app.route('/admin')
def index():
    createDate = db.session.query(member.DateOfCreation, (func.count(member.MEID))).group_by(member.DateOfCreation).all()
    list = []
    for i in createDate:
        dict = {'label': i[0], 'value': i[1]}
        list.append(dict)

    data = json.dumps(list, cls=DateTimeEncoder)
    return render_template('dashboard.html', data=data)

@app.route('/matchRecords')
def matchRecords():
    match = tmatch.query.all()
    return render_template('matchRecords.html', match=match)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/createSubmit', methods=['GET','POST'])
def createSubmit():
    # get value
    cid = request.form.get('cid')
    match_date = request.form.get('match_date')
    matchStatus = request.form.get('matchStatus')
    winner_id = request.form.get('winner_id')
    loser_id = request.form.get('loser_id')
    meid1set1 = request.form.get('meid1set1')
    meid2set1 = request.form.get('meid2set1')
    meid1set2 = request.form.get('meid1set2')
    meid2set2 = request.form.get('meid2set2')
    meid1set3 = request.form.get('meid1set3')
    meid2set3 = request.form.get('meid2set3')

    if winner_id == '':
        winner_id = None
    if loser_id == '':
        loser_id = None
    if meid1set1 == '':
        meid1set1 = None
    if meid2set1 == '':
        meid2set1 = None
    if meid1set2 == '':
        meid1set2 = None
    if meid2set2 == '':
        meid2set2 = None
    if meid1set3 == '':
        meid1set3 = None
    if meid2set3 == '':
        meid2set3 = None

    # error checking
     #maid 系统自己给
     
    # database operation
    match=""
    match = tmatch(CID=cid, DateOfMatch=match_date, MatchStatus=matchStatus, MEID1Set1Score=meid1set1, MEID2Set1Score=meid2set1, 
                MEID1Set2Score=meid1set2, MEID2Set2Score=meid2set2, MEID1Set3Score=meid1set3, MEID2Set3Score=meid2set3, WinnerMEID=winner_id, LoserMEID=loser_id)
    db.session.add(match)
    db.session.commit()
    return render_template('successCreate.html', match=match)


@app.route('/edit', methods=['GET','POST'])
def edit():
    maid = request.args.get('MAID')
    maid = int(maid)
    match = tmatch.query.get(maid)
    matchStatus = match.MatchStatus
    return render_template('edit.html', match=match, matchStatus=matchStatus)

@app.route('/editSubmit', methods=['GET','POST'])
def editSubmit():
    # get value
    maid = request.form.get('mid')
    cid = request.form.get('cid')
    match_date = request.form.get('match_date')
    matchStatus = request.form.get('matchStatus')
    winner_id = request.form.get('winner_id')
    loser_id = request.form.get('loser_id')
    meid1set1 = request.form.get('meid1set1')
    meid2set1 = request.form.get('meid2set1')
    meid1set2 = request.form.get('meid1set2')
    meid2set2 = request.form.get('meid2set2')
    meid1set3 = request.form.get('meid1set3')
    meid2set3 = request.form.get('meid2set3')

    if winner_id == '':
        winner_id = None
    if loser_id == '':
        loser_id = None
    if meid1set1 == '':
        meid1set1 = None
    if meid2set1 == '':
        meid2set1 = None
    if meid1set2 == '':
        meid1set2 = None
    if meid2set2 == '':
        meid2set2 = None
    if meid1set3 == '':
        meid1set3 = None
    if meid2set3 == '':
        meid2set3 = None

    # error check

    #database operation(edit)
    match = tmatch.query.get(maid)

    match.CID=cid
    match.DateOfMatch=match_date
    match.MatchStatus=matchStatus
    match.WinnerMEID=winner_id
    match.LoserMEID=loser_id
    match.MEID1Set1Score=meid1set1
    match.MEID2Set1Score=meid2set1
    match.MEID1Set2Score=meid1set2
    match.MEID2Set2Score=meid2set2
    match.MEID1Set3Score=meid1set3
    match.MEID2Set3Score=meid2set3
    db.session.commit()

    return render_template('successEdit.html', updateMatch=match)

@app.route('/del', methods=['GET','POST'])
def delete_record():
    maid = request.args.get('MAID')
    maid = int(maid)
    deleted_match = tmatch.query.get(maid)
    db.session.delete(deleted_match)
    db.session.commit()
    
    match = tmatch.query.all()
    msg ='You have successfully delete a record with match ID ' + str(maid)
    return render_template('matchRecords.html', match=match, msg=msg)

@app.route('/visual')
def visual():
    return render_template('visual_initial.html')

@app.route('/visualSubmit', methods=['GET','POST'])
def visualSubmit():
    if request.method == "POST":
        data = request.form.get('inputID')
        memberID = int(data)
        # win = tmatch.query.filter(tmatch.WinnerMEID==memberID).all()
        # lose = tmatch.query.filter(tmatch.LoserMEID==memberID).all()
        winLose = tmatch.query.filter(
            (tmatch.WinnerMEID==memberID) |
            (tmatch.LoserMEID==memberID)).all()

        winValue = tmatch.query.filter(tmatch.WinnerMEID==memberID).count()
        loseValue = tmatch.query.filter(tmatch.LoserMEID==memberID).count()
        data = [{'label': 'win', 'value': winValue}, {'label': 'lose', 'value': loseValue}]
        data = json.dumps(data)
        
        return render_template('visual.html', data=data, winLose=winLose, memberID=memberID)


# ======================================================= Membership ================================================== #
# ======================================================= by Shi Haoling ============================================== #
@app.route('/membership_registration')
def membership_registration():
    return render_template('membership_registration.html')


@app.route('/registration_success')
def registration_success():
    return render_template('membership_reg_success')


@app.route('/submit_membership_registration', methods=["GET", "POST"])
def submit_membership_registration():
    # Get the variable and form validation
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    meid = request.form.get('meid')
    msid = request.form.get('msid')
    plan = request.form.get('plan')

    # Form validation
    error = False

    if not meid:
        flash('Please enter your memberid')
        error = True

    if not fname:
        flash('Please enter your FirstName')
        error = True

    if not plan:
        flash('Please select your Membership Plans')
        error = True

    if not error:
        if not msid:
            meid = int(meid)
            plan = int(plan)
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            # dueday = day + 7
            endyear = year + plan
            startdate = f"{year}-{month}-{day}"
            enddate = f"{endyear}-{month}-{day}"
            # duedate = f"{year}-{month}-{dueday}"
            duedate = datetime.datetime.now() + datetime.timedelta(days=7)
            duedate = str(duedate)
            amount = float(plan * 100)
            Membership = membership(
                MEID=meid,
                StartDate=startdate,
                EndDate=enddate,
                InvoiceDate=startdate,
                DueDate=duedate,
                Amount=amount
            )
            payamount = 100 * plan
            tax = payamount * 0.1
            totalpay = payamount + tax
            db.session.add(Membership)
            db.session.commit()
            db.session.refresh(Membership)
            session['msid'] = msid
            flash(f'Your membership ID #{Membership.MSID} is added')
            return render_template('membership_reg_success.html', membership=Membership, tax=tax, totalpay=totalpay, plan=plan)
        else:
            plan = int(plan)
            enddate = db.session.query(membership.EndDate).filter(
                membership.MSID == msid).scalar()
            endyear = enddate.year + plan
            month = enddate.month
            day = enddate.day
            enddate = f"{endyear}-{month}-{day}"
            Membership = membership.query.get(msid)
            Membership.EndDate = enddate
            db.session.commit()
            payamount = 100 * plan
            tax = payamount * 0.1
            totalpay = payamount + tax
            session['msid'] = msid
            flash(
                f"Your Membership ID #{msid}'s EndDate has been extended to {enddate}")
            return render_template('membership_reg_success.html', membership=Membership, tax=tax, totalpay=totalpay, plan=plan)

    return render_template('membership_registration.html', fname=fname, lname=lname, meid=meid, msid=msid, plan=plan)


@app.route('/payment_success', methods=['GET', 'POST'])
def payment_success():
    msid = request.form.get('msid')
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    startdate = f"{year}-{month}-{day}"
    Membership = membership.query.get(msid)
    Membership.PaidDate = startdate
    db.session.commit()
    return render_template('membership_payment_success.html')

@app.route('/extention', methods = ['GET', 'POST'])
def extend():
    meid = session.get('mid')
    plan = request.form.get('plan')
    plan = int(plan)
    meid = int(meid)
    memberships = db.session.query(membership).filter(membership.MEID == meid).all()
    for m in memberships:
        year = int(m.EndDate.year)
        month = int(m.EndDate.month)
        day = int(m.EndDate.day)
        Membership = m
    extended_EndDate = f'{year+plan}-{month}-{day}'
    amount = plan * 100
    paidyear = datetime.datetime.now().year
    paidmonth = datetime.datetime.now().month
    paidday = datetime.datetime.now().day
    paidDate = f'{paidyear}-{paidmonth}-{paidday}'
    Membership.EndDate = extended_EndDate
    Membership.PaidDate = paidDate
    Membership.InvoiceDate = paidDate
    Membership.Amount = amount
    db.session.commit()
    payamount = 100 * plan
    tax = payamount * 0.1
    totalpay = payamount + tax
    return render_template('membership_reg_success.html', membership=Membership, tax=tax, totalpay=totalpay, plan=plan)

@app.route('/judge')
def judge_ms():
    meid = session.get('mid')
    Membership = db.session.query(membership).filter(
        membership.MEID == meid).all()
    if not Membership:
        members = member.query.get(meid)
        return render_template('membership_registration.html', fname=members.FirstName, lname=members.LastName, meid=meid)
    return render_template('membership_extend.html')

###

@app.route('/ask_for_chart')
def chartform():
    Membership = membership.query.all()
    year = sorted(set([m.EndDate.year for m in Membership]))
    return render_template('membership_ask_for_chart.html', year=year)


@app.route('/chart', methods=["GET", "POST"])
def chart():
    Membership = membership.query.all()
    year = int(request.form.get('year'))
    paynum = 0
    unpaynum = 0
    # today = datetime.datetime.now().date()
    for m in Membership:
        amount = int(m.Amount)
        plan = amount / 100
        EndDate = m.EndDate
        PaidDate = m.PaidDate
        PaidJudgeDate = EndDate - datetime.timedelta(days=plan*366)
        allyear = sorted(set([m.EndDate.year for m in Membership]))

        if (m.PaidDate is None or PaidDate < PaidJudgeDate) and (m.EndDate.year == year):
            unpaynum += 1
        elif m.EndDate.year == year:
            paynum += 1
    structure1 = {
        "label": "not pay",
        "value": str(unpaynum)}
    structure2 = {
        "label": "paid",
        "value": str(paynum)
    }
    structure = [structure1, structure2]
    chartData = json.dumps(structure)
    return render_template('membership_chart.html', chartData=chartData, year=year, allyear=allyear)

@app.route('/delete_ms/<int:ms_id>', methods=['POST', 'GET'])
def delete_ms(ms_id):
    Membership = membership.query.get(ms_id)
    if Membership is not None:
        db.session.delete(Membership)
        db.session.commit()
        flash(f"Membership ID #{ms_id} has been deleted successfully.")
    Memberships = membership.query.all()
    now = datetime.datetime.now()
    return render_template('membership_admin_view.html', memberships=Memberships, now=now)

@app.route('/membership_list')
def membership_list():
    Memberships = membership.query.all()
    now = datetime.datetime.now()
    return render_template('membership_admin_view.html', memberships=Memberships, now=now)

@app.route('/search_invoice')
def search_invoice():
    meid = session.get('mid')
    memberships = db.session.query(membership).filter(membership.MEID == meid).all()
    for m in memberships:
        Membership = m
    return render_template('membership_invoice.html', membership=Membership)