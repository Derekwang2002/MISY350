# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app import db

class Member(db.Model):
    MEID = db.Column(db.Integer, primary_key=True)

class Match(db.Model):
    MAID = db.Column(db.Integer, primary_key=True)

class Challenge(db.Model):
    CID = db.Column(db.Integer, primary_key=True)
    ChallengerMEID = db.Column(db.Integer, nullable=False)
    ChallengedMEID = db.Column(db.Integer, nullable=False)
    DateOfChallenge = db.Column(db.Date, nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    Notes = db.Column(db.String(100), nullable=True)

class Membership(db.Model):
    MSID = db.Column(db.Integer, primary_key=True)

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
