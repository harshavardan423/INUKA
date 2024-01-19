# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
import os
from sqlalchemy import create_engine,PickleType
from sqlalchemy.exc import ProgrammingError
from flask_login import UserMixin


# Replace [USERNAME] and [PASSWORD] with your actual environment variable names
username = os.getenv("DB_USERNAME")
password =os.getenv("DB_PASSWORD")

print("USERNAME : "  + username)
print("PASSWORD : "  + password)


# Check if username and password are provided
if username is None or password is None:
    raise ValueError("Database username and password are required.")

# Construct the connection string
if os.getenv("DEBUG") == "TRUE":
    # Use SQLite for development/debugging
    engine = create_engine('sqlite:///inuka_db.sqlite3')
    print("DB : DEV")
else:
    # Use MySQL for production
    connection_string = f"mysql+mysqlconnector://{username}:{password}@aws.connect.psdb.cloud:3306/inuka"
    engine = create_engine(connection_string, echo=True)
    print("DB : PROD")

print(engine)

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active_sessions = db.Column(PickleType, default=set)

class InsightsPost(db.Model):
    __tablename__ = 'insights_post'

    id = db.Column(db.String(500), primary_key=True)
    member_name = db.Column(db.String(500))
    links = db.Column(db.String(500))
    spotify_link = db.Column(db.String(500))
    apple_music_link = db.Column(db.String(500))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    quote = db.Column(db.String(500))
    image = db.Column(db.String(500))

class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.String(500), primary_key=True)
    member_name = db.Column(db.String(500))
    member_heading = db.Column(db.String(500))
    text = db.Column(db.String(2000))
    profile_image = db.Column(db.String(500))

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.String(500), primary_key=True)
    title = db.Column(db.String(100))
    title_2 = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    short_description = db.Column(db.String(1500))
    skills = db.Column(db.String(1000))

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.String(500), primary_key=True)
    text = db.Column(db.String(500))
    default_answer = db.Column(db.String(50))
    job_id = db.Column(db.String(500))

class Applicant(db.Model):
    __tablename__ = 'applicant'
    
    id = db.Column(db.String(500), primary_key=True)
    name = db.Column(db.String(500))
    email = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    resume = db.Column(db.String(500))
    job_id = db.Column(db.String(500))
    previous_job = db.Column(db.String(500))
    previous_job_location = db.Column(db.String(500))

class Answer(db.Model):
    __tablename__ = 'answer'
    
    id = db.Column(db.String(500), primary_key=True)
    applicant_id = db.Column(db.String(500))
    question_id = db.Column(db.String(500))
    answer_text = db.Column(db.String(500))



# try :
#     with engine.connect() as connection:
#         connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
#         connection.execute(text("CREATE TABLE newtable_2 (id INTEGER, name VARCHAR(20))"))

#         connection.execute(text("DROP TABLE answer"))
#         connection.execute(text("DROP TABLE applicant"))
#         connection.execute(text("DROP TABLE insights_post"))
#         connection.execute(text("DROP TABLE job"))
#         connection.execute(text("DROP TABLE question"))
#         connection.execute(text("DROP TABLE team_member"))
#         print("DELETED TABLES")

#     connection.execute(text("DROP TABLE example"))
#     connection.execute(text("DROP TABLE newtable"))
# except ProgrammingError as e:
#     print(f"An error occurred: {e}")




    
