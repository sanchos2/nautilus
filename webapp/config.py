import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
print(SQLALCHEMY_DATABASE_URI)
TEXT = 'Привет из config.py!'
DEBUG = True
