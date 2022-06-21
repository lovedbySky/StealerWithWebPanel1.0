import sys, os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


__version__ = '1.0.0'
app = Flask(__name__)
uri = 'sqlite:///../steal.db'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = 'rjngkajdrngjnarj;g'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import_path = os.getcwd()
import_path =os.path.join(import_path, '..')
sys.path.append(import_path)


import config

from panel import models, routers
