import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@db/elocompare'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
