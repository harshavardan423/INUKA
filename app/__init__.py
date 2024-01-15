from flask import Flask
from .models import db  # Use a relative import
import json
import secrets
from dotenv import load_dotenv
import MySQLdb
import os

# Generate a random hex string of 24 bytes (48 characters)
secret_key = secrets.token_hex(24)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inuka_db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = secret_key  # Set a strong and secure secret key


app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure MySQL connection
connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "/etc/ssl/certs/ca-certificate.crt"
    }
)

# Set Flask app configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + os.getenv("DB_USERNAME") + ":" + os.getenv("DB_PASSWORD") + "@" + os.getenv("DB_HOST") + "/" + os.getenv("DB_NAME")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Import your routes after initializing the app
from . import routes  # Use a relative import

# Create tables when the application starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
