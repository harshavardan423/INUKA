from flask import Flask, render_template,request,jsonify,redirect,url_for,send_file,flash,session
from flask_wtf.csrf import generate_csrf
import json
from .models import db,User, InsightsPost, Job, Applicant, TeamMember, Question, Answer,engine
from . import app
import os
from werkzeug.utils import secure_filename
from base64 import b64encode
from sqlalchemy import func
from sqlalchemy.orm import Session
import io
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user
import time
import random
import cloudinary
import cloudinary.uploader 
import cloudinary.api


cloudinary.config( 
  cloud_name = "dhkcm3uf7", 
  api_key = "164591798326994", 
  api_secret = "dFKTMhOH76tleFb2N4sAGludOrE" 
)

# Example data store to keep track of active sessions
active_sessions_per_user = {}

def as_fraction(ratio):
    from fractions import Fraction
    return str(Fraction(ratio).limit_denominator())

app.jinja_env.filters['as_fraction'] = as_fraction

# Register a custom filter function for base64 encoding
def b64encode_filter(data):
    return b64encode(data).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode_filter


login_manager = LoginManager(app)

# Initialize Flask-Login
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    # Replace this with your actual user lookup logic
    return User.query.get(int(user_id))


# Handle unauthorized access by redirecting to the login page
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'warning')
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and user.password == password:
                login_user(user)

                # Storing user information in session
                session['user_id'] = user.id

                # Add the session ID to the user's active sessions
                user.add_active_session(session['_id'])

                return redirect(url_for('dashboard'))

        return render_template('login.html')
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    members = TeamMember.query.all()
    return render_template('about_us.html', members = members)


@app.route('/inuka_insights')
def inuka_insights():
    try:
        # Assuming you have a query to get Inuka posts, adjust it based on your model and database structure
        inuka_posts = InsightsPost.query.all()

        return render_template('inuka_insights.html', insights_posts=inuka_posts)
    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {str(e)}")
        # Return a generic error page or handle it as per your application's requirements
        return render_template('error.html'), 500



@app.route('/contact')
def contact():
    with Session(engine) as session:
        jobs = Job.query.all()
    return render_template('contact_us.html', jobs = jobs)

@app.route('/insights_member_page.html/<int:member_id>')
def insights_member_page(member_id):
    # Find the member with the specified ID
    # member = next((m for m in insights_members["teamMembers"] if m["id"] == member_id), None)
    inuka_post = InsightsPost.query.filter_by(id=member_id).first()
    return render_template('insights_member_page_2.html', member=inuka_post)
    # if member:  
    #     return render_template('insights_member_page.html', member=member)
    # else:
    #     # Handle the case when the member is not found
    #     return render_template('insights_member_page_2.html', post=inuka_post)



# Protected dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    sid = request.args.get('sid')
    print("Reached the dashboard route")
    
    # Check if the current session ID is in the user's active sessions
    print(f"Current User: {current_user.username}")

    # Add any additional debug statements as needed

    return render_template('main_dashboard.html', sid=sid, user=current_user)
    

@app.route('/dashboard/jobs')
@login_required
def jobs_dashboard():
    search_query = request.args.get('search_query', '')

    if search_query:
        # Perform a search based on the query
        jobs = Job.query.filter(Job.title.ilike(f'%{search_query}%')).all()
    else:
        # If no search query, fetch all jobs
        jobs = Job.query.all()

    # Retrieve the count of applicants for each job
    job_applicants_count = (
        db.session.query(Applicant.job_id, func.count(Applicant.id))
        .group_by(Applicant.job_id)
        .all()
    )

    # Create a dictionary to store the count of applicants for each job
    job_applicants_count_dict = {job_id: count for job_id, count in job_applicants_count}

    return render_template('jobs_dashboard.html', jobs=jobs, job_applicants_count=job_applicants_count_dict,user=current_user)
    


# Use the app context
# with app.app_context():
#     # Generate a unique ID for Job using a combination of timestamp and random number
#     job_id = f"{int(time.time())}{random.randint(1000, 9999)}"

#     # Create a dummy Job with the generated ID
#     dummy_job = Job(
#         id=job_id,
#         title="Software Developer",
#         title_2="Backend Engineer",
#         description="Job description for a software developer",
#         short_description="Backend development position",
#         skills="Python, Django, SQL"
#     )

#     # Add the dummy Job to the database session
#     db.session.add(dummy_job)

#     # Commit the changes to persist the dummy Job to the database
#     db.session.commit()

#     # Optional: Print the ID of the newly created dummy Job
#     print("Dummy Job ID:", dummy_job.id)

#     # Generate a unique ID for Question using a combination of timestamp and random number
#     question_id = f"{int(time.time())}{random.randint(1000, 9999)}"

#     # Create a dummy Question with the generated ID and associate it with the dummy Job
#     dummy_question = Question(
#         id=question_id,
#         text="What programming languages do you prefer?",
#         default_answer="Python",
#         job_id=job_id  # Linking the Question to the Job using its ID
#     )

#     # Add the dummy Question to the database session
#     db.session.add(dummy_question)

#     # Commit the changes to persist the dummy Question to the database
#     db.session.commit()

#     # Optional: Print the ID of the newly created dummy Question
#     print("Dummy Question ID:", dummy_question.id)

@app.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():

    if request.method == 'POST':
        job_id = f"{int(time.time())}{random.randint(1000, 9999)}"

        # Get data from the form
        title = request.form.get('title')
        title_2 = request.form.get('title_2')
        skills = request.form.get('skills')
        description = request.form.get('description')
        short_description = request.form.get('short_description')

        questions = request.form.getlist('questions[]')  # Get a list of questions from the form
        default_answers = request.form.getlist('default_answers[]')  # Get a list of default answers from the form
        with Session(engine) as session:

            # Create a new job
            new_job = Job(title=title, title_2=title_2, skills=skills, description=description, short_description=short_description,id=job_id)
            db.session.add(new_job)
            db.session.commit()

            question_id = f"{int(time.time())}{random.randint(1000, 9999)}"
            # Save questions and default answers to the database
            for question_text, default_answer_text in zip(questions, default_answers):
                new_question = Question(text=question_text, job_id=job_id,default_answer=default_answer_text,id=question_id)
                db.session.add(new_question)

            db.session.commit()

        # Redirect to the jobs dashboard or any other desired page
        return redirect(url_for('jobs_dashboard'))

    # Render the create job form for GET requests
    return render_template('create_job.html')


@app.route('/edit_job/<string:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get(job_id)
    
    # Manually query for questions associated with the job
    questions = Question.query.filter_by(job_id=job_id).all()
    
    if request.method == 'GET':
        return render_template('edit_job.html', job=job, questions=questions)

    if request.method == 'POST':
        with Session(engine) as session:
            # Update job details
            print("Before update:")
            print("Job ID:", job.id)
            print("Job Title:", job.title)

            job.title = request.form['title']
            job.title_2 = request.form['title_2']
            job.skills = request.form['skills']
            job.description = request.form['description']
            job.short_description = request.form['short_description']

            # Update existing questions and default answers
            updated_existing_questions = request.form.getlist('existing_questions[]')
            updated_existing_default_answers = request.form.getlist('existing_default_answers[]')

            for question in questions:
                if question.text in updated_existing_questions:
                    index = updated_existing_questions.index(question.text)
                    question.default_answer = updated_existing_default_answers[index]
                else:
                    db.session.delete(question)

            # Add new questions and default answers
            new_questions = request.form.getlist('questions[]')
            new_default_answers = request.form.getlist('new_default_answers_1[]')
            question_id = f"{int(time.time())}{random.randint(1000, 9999)}"
            for question_text, default_answer_text in zip(new_questions, new_default_answers):
                new_question = Question(text=question_text, id=question_id, default_answer=default_answer_text, job_id=job.id)
                db.session.add(new_question)

            db.session.commit()


            # Re-query the job after committing changes
            job = Job.query.get(job_id)

            print("After update:")
            print("Job ID:", job.id)
            print("Job Title:", job.title)

            # Redirect to the jobs dashboard or any other desired page
            return redirect(url_for('jobs_dashboard'))
    
    # Render the edit job form for GET requests
    return render_template('edit_job.html', job=job, questions=questions)



# Route to delete a job
@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):

    job = Job.query.get(job_id)
    with Session(engine) as session:

        if request.method == 'GET':
            return render_template('delete_job.html', job=job)

        elif request.method == 'POST':
            applicants = Applicant.query.filter_by(job_id=job_id).all()
            # remove applicant associations with job
            for applicant in applicants:
                applicant.job_id = None

            questions = Question.query.filter_by(job_id=job_id).all()

            # remove questions associations with job
            for question in questions:
                question.job_id = None

            db.session.delete(job)
            db.session.commit()
            return redirect(url_for('jobs_dashboard'))  # Redirect to jobs dashboard after deleting


@app.route('/submit_application/<int:job_id>', methods=['POST'])
def submit_application(job_id):
    apply_id = f"{int(time.time())}{random.randint(1000, 9999)}"

    # Get data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    previous_job = request.form.get('previous_job')
    previous_job_location = request.form.get('previous_job_location')

    # Handle file upload for the resume
    resume_file = request.files.get('resume')
    resume_data = resume_file.read() if resume_file else None

    # Upload the resume file to Cloudinary
    if resume_data:
        cloudinary_response = cloudinary.uploader.upload(resume_data, resource_type="raw")
        resume_url = cloudinary_response['url']  # Use the URL, not the CloudinaryResource

        # Update the Applicant model with the Cloudinary URL
        new_applicant = Applicant(id=apply_id, name=name, email=email, phone=phone, job_id=job_id,
                                  previous_job=previous_job, previous_job_location=previous_job_location,
                                  resume=resume_url)
        db.session.add(new_applicant)
        db.session.commit()

        # Redirect to a confirmation page or any other desired page
        return redirect(url_for('application_confirmation', job_id=job_id))

    # Handle the case when no resume file is provided
    # Redirect or display an error message as needed
    return render_template('error.html', message='No resume file provided')



# Add this route to your Flask application
@app.route('/application_form/<int:job_id>')
def application_form(job_id):
    job = Job.query.get(job_id)
    questions = Question.query.filter_by(job_id=job_id).all()
    return render_template('application_form.html', job=job, questions=questions)

# Add this route to your Flask application
@app.route('/view_job/<int:job_id>')
def view_job(job_id):
    job = Job.query.get(job_id)
    return render_template('view_job.html', job=job)



@app.route('/view_applicants/<int:job_id>')
@login_required
def view_applicants(job_id):
    with Session(engine) as session:
        job = Job.query.get(job_id)
        
        questions = Question.query.filter_by(job_id=job_id).all()
        # Query applicants directly based on job_id
        applicants = Applicant.query.filter_by(job_id=job_id).all()

        correct_answers_ratio = []

        for applicant in applicants:
            correct_answers_count = 0
            total_questions = len(questions)

            for question in questions:
                answer = Answer.query.filter_by(applicant_id=applicant.id, question_id=question.id).first()

                if answer and answer.answer_text.lower() == question.default_answer.lower():
                    correct_answers_count += 1

            ratio = correct_answers_count / total_questions if total_questions > 0 else 0
            correct_answers_ratio.append((applicant, ratio))

    return render_template('view_applicants.html', job=job, correct_answers_ratio=correct_answers_ratio, applicants=applicants)



@app.route('/view_job_applicant/<int:job_id>/<int:applicant_id>')
@login_required
def view_job_applicant(job_id, applicant_id):
    job = Job.query.get(job_id)
    applicant = Applicant.query.get(applicant_id)
    questions = Question.query.filter_by(job_id=job_id).all()
    
    # Fetch job questions and applicant answers
    job_questions = questions
    applicant_answers = Answer.query.filter_by(applicant_id=applicant.id).all()
    
    return render_template('view_job_applicant.html', job=job, applicant=applicant, job_questions=job_questions, applicant_answers=applicant_answers)

@app.route('/view_applicant/<int:applicant_id>')
@login_required
def view_applicant(applicant_id):
    applicant = Applicant.query.get(applicant_id)

    # Get the jobs applied by the applicant
    jobs_applied = Job.query.filter_by(id=applicant.job_id).all()

    # Get the answers for the questions related to the jobs applied by the applicant
    answers = Answer.query.filter(Answer.applicant_id == applicant_id).all()

    return render_template('view_applicant.html', applicant=applicant, jobs_applied=jobs_applied, answers=answers)

@app.route('/view_all_applicants')
@login_required
def view_all_applicants():
    search_query = request.args.get('search_query', '')
    
    if search_query:
        # Perform a search based on the query
        applicants = Applicant.query.filter(
            (Applicant.name.ilike(f'%{search_query}%')) |
            (Applicant.email.ilike(f'%{search_query}%')) |
            (Applicant.phone.ilike(f'%{search_query}%'))
        ).all()
    else:
        # If no search query, fetch all applicants
        applicants = Applicant.query.all()
    
    return render_template('view_all_applicants.html', applicants=applicants)





@app.route('/download_resume/<int:applicant_id>')
@login_required
def download_resume(applicant_id):
    applicant = Applicant.query.get(applicant_id)

    if applicant and applicant.resume:
        resume_url = applicant.resume
        return redirect(resume_url)
    else:
        flash('Resume not found.', 'danger')
        return redirect(url_for('index'))  # Redirect to an appropriate page if resume is not found
    
# Route to render the members dashboard page
@app.route('/dashboard/team_members')
@login_required
def team_members_dashboard():
    team_members = TeamMember.query.all()
    return render_template('team_members_dashboard.html', team_members=team_members)


@app.route('/create_team_member', methods=['GET', 'POST'])
@login_required
def create_team_member():
    if request.method == 'POST':
        with Session(engine) as session:
            member_id = f"{int(time.time())}{random.randint(1000, 9999)}"
            
            # Get data from the form
            member_name = request.form.get('member_name')
            member_heading = request.form.get('member_heading')
            text = request.form.get('text')

            # Check if a file was uploaded
            if 'profile_image' in request.files:
                profile_image_file = request.files['profile_image']
                
                # Check if the file is an allowed type (e.g., image)
                allowed_types = {'png', 'jpg', 'jpeg', 'gif'}
                if profile_image_file.filename.split('.')[-1].lower() not in allowed_types:
                    flash('Please upload a valid image file (png, jpg, jpeg, gif).', 'danger')
                    return redirect(url_for('create_team_member'))

                # Upload the profile image file to Cloudinary
                profile_image_data = profile_image_file.read()
                cloudinary_response = cloudinary.uploader.upload(profile_image_data, folder='team_member_images')
                profile_image_url = cloudinary_response['secure_url']
            else:
                profile_image_url = None

            # Create a new team member
            new_member = TeamMember(
                member_name=member_name, id=member_id, member_heading=member_heading,
                text=text, profile_image=profile_image_url
            )

            db.session.add(new_member)
            db.session.commit()

            # Redirect to the team members dashboard or any other desired page
            return redirect(url_for('team_members_dashboard'))

    # Render the create team member form for GET requests
    return render_template('create_team_member.html')



# Assuming you already have the TeamMember model defined

@app.route('/edit_team_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_team_member(member_id):
    with Session(engine) as session:
        team_member = TeamMember.query.get(member_id)

        if request.method == 'POST':
            # Update the team member data
            team_member.member_name = request.form.get('member_name')
            team_member.member_heading = request.form.get('member_heading')
            team_member.text = request.form.get('text')

            # Handle profile image update
            new_profile_image = request.files['profile_image']
            
            if new_profile_image:
                # Check if the file is an allowed type (e.g., image)
                allowed_types = {'png', 'jpg', 'jpeg', 'gif'}
                if new_profile_image.filename.split('.')[-1].lower() not in allowed_types:
                    # flash('Please upload a valid image file (png, jpg, jpeg, gif).', 'danger')
                    return redirect(url_for('edit_team_member', member_id=member_id))

                # Upload the new profile image file to Cloudinary
                new_profile_image_data = new_profile_image.read()
                cloudinary_response = cloudinary.uploader.upload(new_profile_image_data, folder='team_member_images')
                team_member.profile_image = cloudinary_response['secure_url']

            db.session.commit()

            # Redirect to the team members dashboard or any other desired page
            return redirect(url_for('team_members_dashboard'))

    # Render the edit team member form for GET requests
    return render_template('edit_team_member.html', team_member=team_member)


# Route to delete a team member
@app.route('/delete_team_member/<int:member_id>', methods=['POST'])
@login_required
def delete_team_member(member_id):
    member = TeamMember.query.get(member_id)
    with Session(engine) as session :

        if not member:
            return jsonify({'message': 'Team member not found'}), 404

        db.session.delete(member)
        db.session.commit()

    return redirect(url_for('team_members_dashboard'))  # Redirect to team members dashboard after deleting



# Route to render the Insights posts dashboard page
@app.route('/dashboard/insights_posts')
@login_required
def insights_posts_dashboard():
    insights_posts = InsightsPost.query.all()
    return render_template('insights_posts_dashboard.html', insights_posts=insights_posts)



@app.route('/create_insights_post', methods=['GET', 'POST'])
@login_required
def create_insights_post():
    with Session(engine) as session :
        if request.method == 'POST':
            post_id = f"{int(time.time())}{random.randint(1000, 9999)}"
            # Get data from the form
            member_name = request.form.get('member_name')
            links = request.form.get('links')
            title = request.form.get('title')
            description = request.form.get('description')
            quote = request.form.get('quote')
            spotify_link = request.form.get('spotify_link')
            apple_music_link = request.form.get('apple_music_link')

            # Handle file upload for image
            if 'image' in request.files:
                image_file = request.files['image']
                
                # Check if the file is an allowed type (e.g., image)
                allowed_types = {'png', 'jpg', 'jpeg', 'gif'}
                if image_file.filename.split('.')[-1].lower() not in allowed_types:
                    # flash('Please upload a valid image file (png, jpg, jpeg, gif).', 'danger')
                    return redirect(url_for('create_insights_post'))

                # Upload the image file to Cloudinary
                image_data = image_file.read()
                cloudinary_response = cloudinary.uploader.upload(image_data, folder='insights_post_images')
                image_url = cloudinary_response['secure_url']
            else:
                image_url = None

            # Create a new Insights post with the image URL
            new_post = InsightsPost(
                id=post_id, member_name=member_name, links=links, spotify_link=spotify_link,
                apple_music_link=apple_music_link, title=title, description=description, quote=quote, image=image_url
            )
            db.session.add(new_post)
            db.session.commit()

            # Redirect to the Insights posts dashboard or any other desired page
            return redirect(url_for('insights_posts_dashboard'))

    # Render the create Insights post form for GET requests
    return render_template('create_insights_post.html')


# Route to create a new Insights post
# @app.route('/create_insights_post', methods=['GET', 'POST'])
# def create_insights_post():
#     if request.method == 'POST':
#         # Get data from the form
#         member_name = request.form.get('member_name')
#         links = request.form.get('links')
#         text = request.form.get('text')
#         quote = request.form.get('quote')

#         # Handle file upload for image
#         if 'image' in request.files:
#             image_file = request.files['image']
#             image_data = image_file.read()  # Read the image file as bytes
#         else:
#             image_data = None

#         # Create a new Insights post
#         new_post = InsightsPost(member_name=member_name, links=links, text=text, quote=quote, image=image_data)
#         db.session.add(new_post)
#         db.session.commit()

#         # Redirect to the Insights posts dashboard or any other desired page
#         return redirect(url_for('insights_posts_dashboard'))

#     # Render the create Insights post form for GET requests
#     return render_template('create_insights_post.html')

@app.route('/edit_insights_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_insights_post(post_id):
    with Session(engine) as session :
        insights_post = InsightsPost.query.get_or_404(post_id)

        if request.method == 'POST':
            # Update data from the form
            insights_post.member_name = request.form.get('member_name')
            insights_post.links = request.form.get('links')
            insights_post.spotify_link = request.form.get('spotify_link')
            insights_post.apple_music_link = request.form.get('apple_music_link')
            insights_post.title = request.form.get('title')
            insights_post.description = request.form.get('description')
            insights_post.quote = request.form.get('quote')

            # Handle file upload for image
            image_file = request.files.get('image')
            if image_file:
                # Check if the file is an allowed type (e.g., image)
                allowed_types = {'png', 'jpg', 'jpeg', 'gif'}
                if image_file.filename.split('.')[-1].lower() not in allowed_types:
                    # flash('Please upload a valid image file (png, jpg, jpeg, gif).', 'danger')
                    return redirect(url_for('create_insights_post'))

                # Upload the image file to Cloudinary
                image_data = image_file.read()
                cloudinary_response = cloudinary.uploader.upload(image_data, folder='insights_post_images')
                image_url = cloudinary_response['secure_url']

                # Update the image attribute
                insights_post.image = image_url

            db.session.commit()
            return redirect(url_for('insights_posts_dashboard'))

    return render_template('edit_insights_post.html', insights_post=insights_post)



# Route to delete an Insights post
@app.route('/delete_insights_post/<int:post_id>', methods=['POST'])
@login_required
def delete_insights_post(post_id):
    insights_post = InsightsPost.query.get(post_id)
    db.session.delete(insights_post)
    db.session.commit()
    return redirect(url_for('insights_posts_dashboard'))




# Create, Read, Update, Delete (CRUD) operations for TeamMember
@app.route('/team_members', methods=['GET', 'POST'])
@login_required
def team_members():
    if request.method == 'GET':
        members_list = TeamMember.query.all()
        return jsonify([member.__dict__ for member in members_list])

    elif request.method == 'POST':
        data = request.json
        new_member = TeamMember(**data)
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Team member created successfully'}), 201


@app.route('/team_members/<int:member_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def team_member(member_id):
    member = TeamMember.query.get(member_id)

    if request.method == 'GET':
        return jsonify(member.__dict__)

    elif request.method == 'PUT':
        data = request.json
        member.member_name = data['member_name']
        member.member_heading = data['member_heading']
        member.text = data['text']
        db.session.commit()
        return jsonify({'message': 'Team member updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Team member deleted successfully'})





# Create, Read, Update, Delete (CRUD) operations for InsightsPost
@app.route('/insights_posts', methods=['GET', 'POST'])
@login_required
def insights_posts():
    if request.method == 'GET':
        posts = InsightsPost.query.all()
        return jsonify([post.__dict__ for post in posts])

    elif request.method == 'POST':
        data = request.json
        new_post = InsightsPost(**data)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully'}), 201


@app.route('/insights_posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def insights_post(post_id):
    post = InsightsPost.query.get(post_id)

    if request.method == 'GET':
        return jsonify(post.__dict__)

    elif request.method == 'PUT':
        data = request.json
        post.member_name = data['member_name']
        post.links = data['links']
        post.text = data['text']
        post.quote = data['quote']
        post.image = data['image']
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
    
# CRUD operations for Jobs
@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    if request.method == 'GET':
        jobs_list = Job.query.all()
        return jsonify([job.__dict__ for job in jobs_list])

    elif request.method == 'POST':
        data = request.json
        new_job = Job(**data)
        db.session.add(new_job)
        db.session.commit()
        return jsonify({'message': 'Job created successfully'}), 201


@app.route('/jobs/<int:job_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def job(job_id):
    job = Job.query.get(job_id)

    if request.method == 'GET':
        return jsonify(job.__dict__)

    elif request.method == 'PUT':
        data = request.json
        job.title = data['title']
        db.session.commit()
        return jsonify({'message': 'Job updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job deleted successfully'})