# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session, flash
from jinja2  import TemplateNotFound

# App modules
from app import app, db
# from app.models import Profiles
from app.models import Suppliers, Products

# App main route + generic routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitted')
def supplier():
    return render_template('HW6Q1.2.html')

@app.route('/new_product', methods = ['get', 'post'])
def new_product():
    if request.method == 'post':
        pid = request.form.get('productID')
        sid = request.form.get('supplierID')
        cid = request.form.get('categoryID')
        pname = request.form.get('productName')
        ustock = request.form.get('unitStock')
        uprice = request.form.get('unitPrice')
        if len(pid) < 2:
            flash('Please enter something!', category='error')

    suppliers = Suppliers.query.all() # .with_entities(Suppliers.SupplierID)
    return render_template('HW6Q1.html', suppliers=suppliers)



def test():
    fstsid = Suppliers.query.get(1).SupplierID
    print('Successful retireved' + str(fstsid))
    return render_template('HW6Q1.html', fstsid=fstsid)

