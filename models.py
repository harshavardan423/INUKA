# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA


db = SQLAlchemy()

class InsightsPost(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(255))
    member_heading = db.Column(db.String(255))
    text = db.Column(db.String(500))
    profile_image = db.Column(db.LargeBinary)  # BLOB field to store binary image data

    
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    title_2 = db.Column(db.String(50))
    description = db.Column(db.String(255))
    short_description = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    applicants = db.relationship('Applicant', backref='job', lazy=True)
    questions = db.relationship('Question', backref='job', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    default_answer = db.Column(db.String(50))


class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    resume = db.Column(db.LargeBinary)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    previous_job = db.Column(db.String(255))
    previous_job_location = db.Column(db.String(255))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_text = db.Column(db.String(255))
    question = db.relationship('Question', backref='answers', lazy=True)