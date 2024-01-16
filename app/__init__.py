from flask import Flask
from .models import db  # Use a relative import
import json
import secrets
import os

# Replace [USERNAME] and [PASSWORD] with your actual environment variable names
username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")

# Generate a random hex string of 24 bytes (48 characters)
secret_key = secrets.token_hex(24)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inuka_db.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://dj6i4mzw9m8fgyoot4eg:pscale_pw_VyUu9oyp8CZYoXPpY9VuF1RnRzXHMQeza8aPK9lg3MB@aws.connect.psdb.cloud:3306/inuka"

# 'mysql+pymysql://your_planetscale_username:your_planetscale_password@your_planetscale_host:3306/inuka'
# 'sqlite:///inuka_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key  # Set a strong and secure secret key
db.init_app(app)

# Import your routes after initializing the app
from . import routes  # Use a relative import



# Create tables when the application starts
# with app.app_context():
#     db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
