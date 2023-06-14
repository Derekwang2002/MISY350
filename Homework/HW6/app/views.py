# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import re, json
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

# Page for HW6Q1
@app.route('/new_product')
def new_product():
    suppliers = Suppliers.query.all()
    products = Products.query.all()
    pcategories = db.session.query(Products.CategoryID).distinct().all()
    # pcategories = Products.query.with_entities(Products.CategoryID).distinct(Products.CategoryID).all() # has same output
    return render_template('HW6Q1.html', suppliers=suppliers, products=products, pcategories=pcategories)

# page for HW6Q2
@app.route('/log_in')
def log_in():
    return render_template('HW6Q2.html')

# page for HW6Q1
@app.route('/product_view', methods=['GET', 'POST'])
def product_view():
    suppliers = Suppliers.query.all()
    
    # chartData = db.session.query(Products.ProductName.label('label'), (Products.UnitsInStock*Products.UnitPrice).label('value'))
    # chartData = [row._asdict() for row in chartData]
    
    if request.method == 'POST':
        sidChart = request.form.get('supplierID')
        
        if sidChart != '':
            chartDataRaw = db.session.query(Products.ProductName.label('label'), (Products.UnitsInStock*Products.UnitPrice).label('value')).filter(Products.SupplierID==int(sidChart))
            chartDataArray = [row._asdict() for row in chartDataRaw]
            for item in chartDataArray:
                item['value'] = float(item['value'])
            chartData = json.dumps(chartDataArray)
            return render_template('HW7Q1.html', suppliers=suppliers, sidChart=sidChart, chartData=chartData)
        else:
            flash(['Please one supplier!', 'error', 'supplierID'])
            return render_template('HW7Q1.html', suppliers=suppliers)
        
    return render_template('HW7Q1.html', suppliers=suppliers) # , test=chartData

## ========= control ============
@app.route('/submitted', methods = ['GET', 'POST'])
def submitted(): # root function
    if request.method == 'POST':
        suppliers = Suppliers.query.all()
        products = Products.query.all() 
        pcategories = db.session.query(Products.CategoryID).distinct().all() 
        # .order_by(Products.CategoryID.asc()) # distinc() will automatically order

        form_is_valid = True
        pid = request.form.get('productID')
        sid = request.form.get('supplierID')
        cid = request.form.get('categoryID')
        pname = request.form.get('productName')
        ustock = request.form.get('unitStock')
        uprice = request.form.get('unitPrice')

        # form validation
        if pname == '':
            flash(['Please enter Product Name!', 'error', 'productName'])
            form_is_valid = False
        if sid == '':
            flash(['Please enter Supplier ID!', 'error', 'supplierID'])
            form_is_valid = False
        if cid == '':
            flash(['Please enter Category ID!', 'error', 'categoryID'])
            form_is_valid = False
        if uprice == '':
            flash(['Please enter unit price!', 'error', 'unitPrice'])
            form_is_valid = False          
        elif not re.search(r'(^[0-9]\d*\.?\d*$)', uprice): 
            flash(['Positive decimal only!', 'error', 'unitPrice'])
            form_is_valid = False
        if ustock == '':
            flash(['Please enter unit in stock!', 'error', 'unitStock'])
            form_is_valid = False
        elif not re.search(r'^\d*$', ustock): 
            flash(['Positive integer only!', 'error', 'unitStock'])
            form_is_valid = False

        if not form_is_valid:
            return render_template(
                'HW6Q1.html', 
                suppliers=suppliers, products=products, pcategories=pcategories, 
                pid=pid, sid=sid, cid=cid, pname=pname , ustock=ustock, uprice=uprice
            )
        else:
            ## database operation
            if not pid:
                add_product = Products(ProductName=pname, SupplierID=sid, CategoryID=cid, UnitPrice=uprice, UnitsInStock=ustock)
                db.session.add(add_product)
                db.session.commit()
                db.session.refresh(add_product)
                flash(f'A new product: {pname}(ID:{add_product.ProductID}) is added to the database')
                return render_template(
                    'HW6Q1.2.html',
                    suppliers=suppliers, products=products, pcategories=pcategories, 
                    pid=pid, sid=sid, cid=cid, pname=pname , ustock=ustock, uprice=uprice
                )
            else:
                pid = int(pid)
                existing_product = Products.query.get(pid)
                existing_product.ProductName = pname
                existing_product.SupplierID = sid
                existing_product.CategoryID = cid
                existing_product.UnitPrice = uprice
                existing_product.UnitsInStock = ustock
                db.session.commit()
                flash(f'The product {pname}(ID:{pid}) has been updated')
                return render_template(
                    'HW6Q1.2.html',
                    suppliers=suppliers, products=products, pcategories=pcategories, 
                    pid=pid, sid=sid, cid=cid, pname=pname , ustock=ustock, uprice=uprice
                )

    flash('nothing happened')        
    return render_template('HW6Q1.2.html')

@app.route('/logged', methods = ['GET', 'POST'])
def logged():
    if request.method == 'POST':
        sids = []
        cnames = []
        supplierIDs = db.session.query(Suppliers.SupplierID).all()
        companyNames = db.session.query(Suppliers.CompanyName).all()
        session['loginSupplierID'] = request.form.get('loginSupplierID')
        session['loginCompanyName'] = request.form.get('loginCompanyName')
        form_is_valid = True

        for supplierID in supplierIDs:
            sids.append(supplierID.SupplierID)
        for companyName in companyNames:
            cnames.append(companyName.CompanyName)

        # form validation
        if session.get('loginSupplierID') == '':
            flash(['Please enter ID!', 'error', 'loginSupplierID'])
            form_is_valid = False
        elif int(session.get('loginSupplierID')) not in sids:
            flash(['ID not registered!', 'error', 'loginSupplierID'])
            form_is_valid = False
        if session.get('loginCompanyName') == '':
            flash(['Please enter Name', 'error', 'loginCompanyName'])
            form_is_valid = False  
        elif session.get('loginCompanyName') not in cnames:
            flash(['Name not registered!', 'error', 'loginCompanyName'])
            form_is_valid = False

        if not form_is_valid:
            return render_template(
                'HW6Q2.html',
                sidLogged=session.get('loginSupplierID'), 
                cnameLogged=session.get('loginCompanyName')
            )
        else:
            return render_template(
                'logged.html', 
                sidLogged=session.get('loginSupplierID'), 
                cnameLogged=session.get('loginCompanyName')
            )

    else:
        sidLogged = cnameLogged = '(Get-no-value)'
        return render_template('logged.html', sidLogged=sidLogged, cnameLogged=cnameLogged)

