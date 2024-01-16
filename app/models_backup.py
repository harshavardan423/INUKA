# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text

from sqlalchemy import create_engine
connection_string = "mysql+mysqlconnector://ca0e8ywnnxof110pu46x:pscale_pw_TalLclSTAsu0ikmws676YNXISJMO3BF2uj4XFsFXXoI@aws.connect.psdb.cloud:3306/inuka"
# "mysql+mysqlconnector://ca0e8ywnnxof110pu46x:pscale_pw_TalLclSTAsu0ikmws676YNXISJMO3BF2uj4XFsFXXoI@aws.connect.psdb.cloud:3306/sqlalchemy"
engine = create_engine(connection_string, echo=True)

db = SQLAlchemy()

class InsightsPost(db.Model):
    __tablename__ = 'insights_post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, server_default="7")
    member_name = db.Column(db.String(255))
    links = db.Column(db.String(500))
    spotify_link = db.Column(db.String(500))
    apple_music_link = db.Column(db.String(500))
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    quote = db.Column(db.String(255))
    image = db.Column(db.LargeBinary)   





class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(255))
    member_heading = db.Column(db.String(255))
    text = db.Column(db.String(500))
    profile_image = db.Column(db.LargeBinary)  # BLOB field to store binary image data

    
class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    title_2 = db.Column(db.String(50))
    description = db.Column(db.String(255))
    short_description = db.Column(db.String(100))
    applicants = db.relationship('Applicant', backref='job', lazy=True)
    questions = db.relationship('Question', backref='job', lazy=True)

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    job_id = db.Column(db.Integer)  # No ForeignKey here
    default_answer = db.Column(db.String(50))


class Applicant(db.Model):
    __tablename__ = 'applicant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    resume = db.Column(db.LargeBinary)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    previous_job = db.Column(db.String(255))
    previous_job_location = db.Column(db.String(255))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_text = db.Column(db.String(255))
    question = db.relationship('Question', backref='answers', lazy=True)



# with engine.connect() as connection:
    # connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
    # connection.execute(text("CREATE TABLE newtable (id INTEGER, name VARCHAR(20))"))

   
    # connection.execute(text("DROP TABLE insights_post"))
    # connection.execute(text("DROP TABLE job"))

    # connection.execute(text("DROP TABLE team_member"))
    