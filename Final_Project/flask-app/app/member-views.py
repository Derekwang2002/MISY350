# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session
from jinja2  import TemplateNotFound
import datetime
import json
from sqlalchemy import func

# App modules
from app import app, db
from app.models import member
# from app.models import Profiles

# App main route + generic routing
@app.route('/')
def indexhome():
    #gender ratio
    members_num = member.query.count()
    member_f = member.query.filter(member.Gender=='F').count()
    member_m = member.query.filter(member.Gender=='M').count()
    f_ratio = (member_f/members_num)*100
    m_ratio = (member_m/members_num)*100
    gender_lay = [{'label':'Female',
                      'value': f_ratio},
                      {'label':'Male',
                      'value': m_ratio
                                      }]
    gender_lay = json.dumps(gender_lay)
    # (member.query.group_by(member.Gender).count())/(member.query.all().count())
    
    # gender_layout = db.session.query(member.Gender.label('label'), 
    #                                  (((func.count(member.MEID)).group_by(member.Gender))/((member.MEID).all().count())).label('value'))
    # gender_lay = [row._asdict() for row in gender_layout]
    
    #top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr=order_member[i].UTR
        mid=order_member[i].MEID
        utr_rank = {'label':str(mid), 'value':utr}
        l.append(utr_rank)
    l = json.dumps(l)
    #age group
    all_age = db.session.query(member.Age).all()
    age10=[]
    age20=[]
    age30=[]
    age40=[]
    age50=[]
    age60=[]
    age_group=[]
    for i in all_age:
        if (i[0]>10)&(i[0]<20):
            age10.append(i)
            lb='10+'
            age_group1={'label':lb, 'value':len(age10)}
        elif (i[0]>=20)&(i[0]<30):
            age20.append(i)
            lb='20+'
            age_group2={'label':lb, 'value':len(age20)}
        elif (i[0]>=30)&(i[0]<40):
            age30.append(i)
            lb='30+'
            age_group3={'label':lb, 'value':len(age30)}
        elif (i[0]>=40)&(i[0]<50):
            age40.append(i)
            lb='40+'
            age_group4={'label':lb, 'value':len(age40)}
        elif (i[0]>=50)&(i[0]<60):
            age50.append(i)
            lb='50+'
            age_group5={'label':lb, 'value':len(age50)}
        else:
            age60.append(i)
            lb='60+'
            age_group6={'label':lb, 'value':len(age60)}
    age_group.append(age_group1)
    age_group.append(age_group2)
    age_group.append(age_group3)
    age_group.append(age_group4)
    age_group.append(age_group5)
    age_group.append(age_group6)
    age_group = json.dumps(age_group)
    # age_group = {'label':}
    return render_template('index.html', chartdata1=gender_lay, data2=l, data3=age_group)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('new_register.html')

@app.route('/signup', methods=['GET', 'POST'])
def successfullsignup():
    #get input value
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    email = request.form.get('email')
    pword = request.form.get('password')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    age = request.form.get('age')
    utr = request.form.get('utr')
    #error checking
    error = False
    if len(pword)<=8:
        flash('Please enter a password more than 8 words.')
        error = True
    # if phone.isdigit() == False:
    #     flash('Please enter the phone number with a correct format.')
    #     error = True
    if int(age)<0:
        flash('Age must be greater than 0.')
        error = True
    if float(utr)>16.5 or float(utr)<1:
        flash('The UTR is between 1 and 16.5.')
        error = True
    if not error:
        user=''
        user = member(FirstName=fname, LastName=lname, Email=email, MPassword=pword,Gender=gender,
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
    if currentHour<12:
        greeting = 'Good morning!'
    else:
        greeting = 'Good afternoon!'
    session['now']=datetime.date.today()
    #top utr members
    order_member = member.query.order_by((member.UTR).desc()).all()
    l = []
    for i in range(10):
        # for i in order_member:
        utr=order_member[i].UTR
        mid=order_member[i].MEID
        utr_rank = {'label':str(mid), 'value':utr}
        l.append(utr_rank)
    l = json.dumps(l)

    return render_template('userhome.html', message=greeting, data2=l)

@app.route('/userhomepage', methods=['GET', 'POST'])
def informationSubmit():
    #get input
    username=request.form.get('mid')
    pword=request.form.get('password')
    #valid check
    userinfo = member.query.get(username) #this users whole info
    existing_mid = db.session.query(member.MEID).all()
    existing_mid = [x[0] for x in existing_mid]
    if int(username) in existing_mid:
        if pword == userinfo.MPassword:
            session['mid']=username  #MEID
            session['name']=member.query.get(session['mid']).FirstName
            session['lname']=member.query.get(session['mid']).LastName
            session['email']=member.query.get(session['mid']).Email
            session['phone']=member.query.get(session['mid']).Phone
            session['age']=member.query.get(session['mid']).Age
            session['pword']=member.query.get(session['mid']).MPassword
            session['gender']=member.query.get(session['mid']).Gender
            session['utr']=member.query.get(session['mid']).UTR
            currentHour = datetime.datetime.now().hour
            greeting = ''
            if currentHour<12:
                greeting = 'Good morning!'
            else:
                greeting = 'Good afternoon!'
            #top utr members
            order_member = member.query.order_by((member.UTR).desc()).all()
            l = []
            for i in range(10):
                # for i in order_member:
                utr=order_member[i].UTR
                mid=order_member[i].MEID
                utr_rank = {'label':str(mid), 'value':utr}
                l.append(utr_rank)
            l = json.dumps(l)
            return render_template('userhome.html', message=greeting, data2=l)
        else:
            flash("Error! The password and user does not match! Please try again.")
    else:
        flash('This member dose not exist, please try again!')
    #error checking
    return render_template('new_login.html')

@app.route('/accountsetting')
def account():
    return render_template('account.html')

@app.route('/accountmodify', methods=['GET', 'POST'])
def accountchange():
    #get input
    fname = request.form.get('firstName')
    lname = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phoneNumber')
    gender = request.form.get('gender')
    age = request.form.get('age')
    pword = request.form.get('password')
    #error checking
    error = False
    if len(pword)<=8:
        flash('Please enter a password more than 8 words.')
        error = True
    if phone.isdigit() == False:
        flash('Please enter the phone number with a correct format.')
        error = True
    if int(age)<0:
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
        session['name']=fname
        session['lname']=lname
        session['email']=email
        session['phone']=phone
        session['age']=age
        session['pword']=pword
        session['gender']=gender
        flash('Your information has been updated successfully!')
    return render_template('account.html')

@app.route('/accountdelete')
def aboutdelete():
    return render_template('accountdelete.html')

@app.route('/deleteaccount')
def deleteaccount():
    d_user = member.query.get(session['mid'])
    db.session.delete(d_user)
    db.session.commit()
    return render_template('index.html')

