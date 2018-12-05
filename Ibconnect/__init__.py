import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) 
app.config['SECRET_KEY'] = '~b\xb2\xdfU\x9b\x0e\n\x99\xf5\xb9\xa5 \xc6)\xabo\xd3\x1d.`\xe6\xbd1\xac'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Ibconnect.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

import Ibconnect.models 
import Ibconnect.views