from flask import Flask
from models import db
import json
import secrets



# Generate a random hex string of 24 bytes (48 characters)
secret_key = secrets.token_hex(24)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inuka_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key  # Set a strong and secure secret key
db.init_app(app)



# Import your routes after initializing the app
import routes

# Create tables when the application starts
with app.app_context():
    db.create_all()

    

if __name__ == '__main__':
    app.run(debug=True)
