from datetime import datetime, timedelta

LAMBDA = 0.7
REFRESH_TIME = timedelta(hours = 2)

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secretofmentalbreakdown'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')