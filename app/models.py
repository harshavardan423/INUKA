# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
import os

# Replace [USERNAME] and [PASSWORD] with your actual environment variable names
username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")

print("USERNAME : "  + username)
print("PASSWORD : "  + password)


# Check if username and password are provided
if username is None or password is None:
    raise ValueError("Database username and password are required.")

# Construct the connection string
connection_string = f"mysql+mysqlconnector://nxoptfmnxcjb1z4v7m86:pscale_pw_GjeaCTfDMsU1gS8D1YHsBtjxOOW6rWPcmC7IAh80bxK@aws.connect.psdb.cloud:3306/inuka"


from sqlalchemy import create_engine
# connection_string = "mysql+mysqlconnector://[USERNAME]:[PASSWORD]@aws.connect.psdb.cloud:3306/inuka"
# "mysql+mysqlconnector://ca0e8ywnnxof110pu46x:pscale_pw_TalLclSTAsu0ikmws676YNXISJMO3BF2uj4XFsFXXoI@aws.connect.psdb.cloud:3306/sqlalchemy"
engine = create_engine(connection_string, echo=True)

db = SQLAlchemy()

class InsightsPost(db.Model):
    __tablename__ = 'insights_post'

    id = db.Column(db.String(255), primary_key=True)
    member_name = db.Column(db.String(255))
    links = db.Column(db.String(500))
    spotify_link = db.Column(db.String(500))
    apple_music_link = db.Column(db.String(500))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    quote = db.Column(db.String(255))
    image = db.Column(db.String(255))

class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.String(255), primary_key=True)
    member_name = db.Column(db.String(255))
    member_heading = db.Column(db.String(255))
    text = db.Column(db.String(500))
    profile_image = db.Column(db.String(255))

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(50))
    title_2 = db.Column(db.String(50))
    description = db.Column(db.String(255))
    short_description = db.Column(db.String(100))
    skills = db.Column(db.String(500))

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.String(255), primary_key=True)
    text = db.Column(db.String(255))
    default_answer = db.Column(db.String(50))
    job_id = db.Column(db.String(255))

class Applicant(db.Model):
    __tablename__ = 'applicant'
    
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    resume = db.Column(db.String(255))
    job_id = db.Column(db.String(255))
    previous_job = db.Column(db.String(255))
    previous_job_location = db.Column(db.String(255))

class Answer(db.Model):
    __tablename__ = 'answer'
    
    id = db.Column(db.String(255), primary_key=True)
    applicant_id = db.Column(db.String(255))
    question_id = db.Column(db.String(255))
    answer_text = db.Column(db.String(255))



# with engine.connect() as connection:
    # connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
    # connection.execute(text("CREATE TABLE newtable (id INTEGER, name VARCHAR(20))"))

    # connection.execute(text("DROP TABLE answer"))
    # connection.execute(text("DROP TABLE applicant"))
    # connection.execute(text("DROP TABLE insights_post"))
    # connection.execute(text("DROP TABLE job"))
    # connection.execute(text("DROP TABLE question"))
    # connection.execute(text("DROP TABLE team_member"))

    # connection.execute(text("DROP TABLE example"))
    # connection.execute(text("DROP TABLE newtable"))


    
