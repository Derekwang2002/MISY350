# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import db

class Suppliers(db.Model): # per table 
    SupplierID = db.Column(db.Integer, primary_key=True)
    ProductID = db.relationship('Products') # many to one
    CompanyName = db.Column(db.String(40)) #ForeignKey()
    # ContactName = db.Column(db.String(30), nullable=True)
    # ContactTitle = db.Column(db.String(30), nullable=True)
    # Address = db.Column(db.String(60), nullable=True)
    # City = db.Column(db.String(15), nullable=True)
    # Region = db.Column(db.String(15), nullable=True)
    # PostalCode = db.Column(db.String(10))
    # Country = db.Column(db.String(15), nullable=True)
    # Phone = db.Column(db.String(24), nullable=True)
    # Fax = db.Column(db.String(24), nullable=True)
    # HomaPage = db.Column(db.String, nullable=True)

class Products(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    SupplierID = db.Column(db.Integer, db.ForeignKey('suppliers.SupplierID'))

# class Stats(db.Model):

#     id          = db.Column(db.Integer,   primary_key=True )
#     month       = db.Column(db.String(64),    unique=True  )
#     sold_units  = db.Column(db.Integer                     )
#     total_sales = db.Column(db.Integer                     )

#     def __init__(self, id, month, sold_units, total_sales):
#         self.id          = id
#         self.month       = month
#         self.sold_units  = sold_units
#         self.total_sales = total_sales

#     def __repr__(self):
#         return self.month + ' = ' + str(self.sold_units) + '/ ' + str(self.total_sales)

#     # Optional helper
#     def save(self):

#         # inject self into db session    
#         db.session.add ( self )

#         # commit change and save the object
#         db.session.commit( )

#         return self 
