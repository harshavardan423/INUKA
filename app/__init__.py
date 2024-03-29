from flask import Flask
from .models import db,User  # Use a relative import
import json
import secrets
import os
from flask_session import Session


# Replace [USERNAME] and [PASSWORD] with your actual environment variable names
username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")

# Generate a random hex string of 24 bytes (48 characters)
secret_key = "9ef90a696c47aea69b2f35de9be1f3b3588cfc59518972a0"

app = Flask(__name__)

# Configure Flask app based on DEBUG flag
if os.environ.get("DEBUG") == "TRUE":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inuka_db.sqlite3'
    app.config['DEBUG'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{username}:{password}@aws.connect.psdb.cloud:3306/inuka"
    app.config['DEBUG'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")  # Set a strong and secure secret key
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
db.init_app(app)

# Import your routes after initializing the app
from . import routes  # Use a relative import

# Create tables when the application starts
with app.app_context():
    db.create_all()
    
    
    
    

if __name__ == '__main__':
    app.run(debug=os.environ.get("DEBUG") == "TRUE")
