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

@app.route('/submitted', methods = ['GET', 'POST'])
def submitted(): # root function
    if request.method == 'POST':
        suppliers = Suppliers.query.all()
        productsIDs = Products.query.all()

        form_is_valid = True
        pid = request.form.get('productID')
        sid = request.form.get('supplierID')
        cid = request.form.get('categoryID')
        pname = request.form.get('productName')
        ustock = request.form.get('unitStock')
        uprice = request.form.get('unitPrice')

        if pname == '':
            flash('Please enter Product Name!')
            form_is_valid = False
        if sid == '':
            flash('Please enter Supplier ID!')
            form_is_valid = False
        if cid == '':
            flash('Please enter Category ID!')
            form_is_valid = False
        if uprice == '':
            flash('Please enter unit price!')
            form_is_valid = False          
        elif float(uprice) < 0:
            flash('Please enter positive decimal unit price!')
            form_is_valid = False
        if ustock == '':
            flash('Please enter unit in stock!')
            form_is_valid = False
        elif int(ustock) < 0:
            flash('Please enter positive integer unit in stock!')
            form_is_valid = False

        if not form_is_valid:
            return render_template('HW6Q1.html', suppliers=suppliers, productsIDs=productsIDs)
        else:
            return render_template('HW6Q1.2.html')
            #return redirect(url_for(new_product))

    ## database manipulate
        # if not pid:
        if False:
            add_product = Products(ProductID=pid)
            db.session.add(add_product)
            db.session.commit()
            db.session.refresh(add_product)
            flash(f'A new product: {add_product.ProductID} {pname}')
            return render_template('HW6Q1.2.html')
        elif False:
            pid = int(pid)
            existing_product = Products.query.get(pid)
            existing_product.ProductName = pname
            existing_product.SupplierID = sid
            existing_product.CategoryID = cid
            existing_product.UnitPrice = uprice
            existing_product.UnitInStock = ustock
            db.session.commit()
            flash(f'The product {pname}(ID:{pid}) has been updated')
            return render_template('HW6Q1.2.html')

        
        
    return render_template('HW6Q1.2.html')

# This page is for HW6Q1
@app.route('/new_product', methods = ['GET', 'POST'])
def new_product():
    suppliers = Suppliers.query.all()
    productsIDs = Products.query.all()
    return render_template('HW6Q1.html', suppliers=suppliers, productsIDs=productsIDs)


# def test():
#     fstsid = Suppliers.query.get(1).SupplierID
#     print('Successful retireved' + str(fstsid))
#     return render_template('HW6Q1.html', fstsid=fstsid)

