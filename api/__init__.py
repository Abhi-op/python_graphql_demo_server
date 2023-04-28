from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy





# Initializing our app
app = Flask(__name__)
app.debug = True

CORS(app)

# Configs
# Our database configurations will go here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root%40123@localhost:5432/Demo_Python'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
