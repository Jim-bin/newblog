# -*- coding:utf-8 -*_

import os

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'newblog'
USERNAME = 'root'
PASSWORD = 'root'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_ECHO = True
DEBUG=True

SECRET_KEY = os.urandom(24)
PER_PAGE = 5