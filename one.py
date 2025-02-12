from flask import Flask, render_template, url_for, flash, redirect, request,session, jsonify
from two import Registration, Login, ExamCreationForm, InterestsForm, QuestionForm,ExamResultForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from googletrans import Translator
import os
import speech_recognition as sr
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import openai
app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/examdb"
app.config['SECRET_KEY'] = 'd1aef0865aaaaec841dabcafdeac22aa53b8ebcd4610436c56dd6d105c2561492e8b232b445dac92548e8d59ad0871ed9f'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
@app.route("/submit_voice_answer", methods=["GET", "POST"])
def submit_voice_answer():
    transcript = ""
    score_stage2 = 0

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in the request")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            try:
                # Process and transcribe the audio file
                audioFile = sr.AudioFile(file)
                with audioFile as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, key=None)
                flash("Audio transcription completed successfully", "success")
                
                # Use OpenAI to analyze the answer
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Evaluate the answer: {transcript} based on criteria like relevance, correctness, and depth. Provide a score out of 10.",
                    max_tokens=50
                )
                
                # Extract the score from OpenAI's response
                score_stage2 = int(response.choices[0].text.strip())
                flash(f"Score from Stage 2 (Voice Response): {score_stage2}", "info")
                
            except sr.UnknownValueError:
                transcript = "Audio is not clear enough to transcribe."
                flash("Audio is not clear enough to transcribe.", "error")
            except sr.RequestError:
                transcript = "Could not request results from the service."
                flash("Service is unavailable; please try again later.", "error")

    # Assume `score_stage1` is calculated elsewhere and passed here or stored in the session
    score_stage1 = 5  # Placeholder for example; replace with actual Stage 1 score
    total_score = score_stage1 + score_stage2  # Combine scores from both stages

    return render_template('submit_voice_answer.html', transcript=transcript, total_score=total_score)


# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)


import numpy as np

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# class AudioResponse(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     exam_id = db.Column(db.Integer, nullable=False)
#     question_id = db.Column(db.Integer, nullable=False)
#     file_path = db.Column(db.String(200), nullable=False)
#     confidence = db.Column(db.Float, nullable=False)
#     clarity = db.Column(db.Float, nullable=False)
#     correctness = db.Column(db.Float, nullable=False)


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# def process_audio(file_path):
#     try:
#         y, sr = librosa.load(file_path)
#         mean_audio = np.mean(y)
#         variance_audio = np.var(y)
#         return {
#             'confidence': np.clip(mean_audio / 10, 0, 1),
#             'clarity': np.clip(variance_audio / 1000, 0, 1),
#             'correctness': np.clip(mean_audio / 10, 0, 1)
#         }
#     except Exception as e:
#         print(f"Error processing audio file {file_path}: {e}")
#         return {
#             'confidence': 0.0,
#             'clarity': 0.0,
#             'correctness': 0.0
#         }

# @app.route('/submit_audio/<int:exam_id>/<int:question_id>', methods=['POST'])
# @login_required
# def submit_audio(exam_id, question_id):
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         metrics = process_audio(file_path)

#         audio_response = AudioResponse(
#             user_id=current_user.id,
#             question_id=question_id,
#             exam_id=exam_id,
#             file_path=file_path,
#             confidence=metrics['confidence'],
#             clarity=metrics['clarity'],
#             correctness=metrics['correctness']
#         )
#         db.session.add(audio_response)
#         db.session.commit()

#         return jsonify({'message': 'Audio submitted successfully'}), 200

#     return jsonify({'error': 'Invalid file type'}), 400

# @app.route('/upload_audio', methods=['POST'])
# @login_required
# def upload_audio():
#     if 'audio-file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['audio-file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         metrics = process_audio(file_path)

        # Save metrics and file path to database
        # Example:
        # audio_response = AudioResponse(
        #     user_id=current_user.id,
        #     exam_id=1,  # Replace with actual exam ID
        #     question_id=1,  # Replace with actual question ID
        #     file_path=file_path,
        #     confidence=metrics['confidence'],
        #     clarity=metrics['clarity'],
        #     correctness=metrics['correctness']
        # )
        # db.session.add(audio_response)
        # db.session.commit()

    #     return jsonify({'message': 'Audio submitted successfully'}), 200

    # return jsonify({'error': 'Invalid file type'}), 400



# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


    
class SkippedQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_id = db.Column(db.Integer)

class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=True)  # Optional feedback
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exam = db.relationship('Exam', backref=db.backref('results', lazy=True))
    student = db.relationship('User', backref=db.backref('results', lazy=True))


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    interests = db.Column(db.Text)
    language = db.Column(db.String(20), nullable=True)
    last_interests_update = db.Column(db.DateTime, nullable=True)  # New field
    selected_language = db.Column(db.String(10),nullable=True)  # Add this line
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Stores options as a JSON object
    answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    exam = db.relationship('Exam', back_populates='questions')

class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    exam_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    exam_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.relationship('User', backref='exams')
    course = db.relationship('Course', backref='exams')
    questions = db.relationship('Question', back_populates='exam', lazy=True)
    interests = db.Column(db.Text, nullable=True)  # Store selected interests as a comma-separated string
   
class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('exam_questions'))

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)



    
@app.route("/test_auth")
@login_required
def test_auth():
    return f"Hello, {current_user.username}!"

@app.route("/home")
def home():
    return render_template('home.html')


# Do not call app.run() here in production
# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)

@app.route("/", methods=['GET', 'POST'])    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            role = form.role.data
            login_user(user, remember=form.cookie.data)
            
            # Clear interests and update timestamp to ensure redirection
            user.interests = None
            user.last_interests_update = datetime.utcnow()
            db.session.commit()
            
            if role == 'admin' and user.is_admin:
                flash('Logged in successfully as Admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            elif role == 'student' and not user.is_admin:
                flash('Logged in successfully as Student!', 'success')
                return redirect(url_for('enter_interests'))
            else:
                flash('Invalid role selected.', 'danger')
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Registration()  # Ensure you're using the correct form class here
    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Check for existing admin if the role is admin
        if form.role.data == 'admin':
            existing_admin = User.query.filter_by(is_admin=True).first()
            if existing_admin:
                flash('An admin already exists. Please register as a student.', 'danger')
                return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create a new user
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        role=form.role.data)  # Make sure your User model has a role field
        
        # Set admin flag if the role is admin
        if form.role.data == 'admin':
            new_user.is_admin = True

        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/results/<int:exam_id>")
@login_required
def results(exam_id):
    # Fetch the result for the current user and exam
    result = ExamResult.query.filter_by(exam_id=exam_id, student_id=current_user.id).first()
    exam = Exam.query.get(exam_id)

    if not result or not exam:
        flash('Result not found!', 'error')
        return redirect(url_for('home'))

    return render_template('results.html', score=result.score, total_questions=len(exam.questions))


@app.route ('/student_dashboard')
@login_required
def student_dashboard():
    
    if current_user.role == 'student':
        if not current_user.interests or len(current_user.interests.strip()) == 0:
            flash('Please enter your interests first.', 'warning')
            return redirect(url_for('enter_interests'))
        
        user_interests_list = current_user.interests.split(',')
        
        # Filter exams based on the interests
        filters = [Exam.description.like(f"%{interest.strip()}%") for interest in user_interests_list]
        if filters:
            exams = Exam.query.filter(db.or_(*filters)).all()
        else:
            exams = []

        return render_template('student_dashboard.html', exams=exams)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

# @app.route("/exam_creation", methods=['GET', 'POST'])
# @login_required
# def exam_creation():
#     if not current_user.is_admin:
#         flash('Only admins can create exams.', 'danger')
#         return redirect(url_for('login'))
    
#     form = ExamCreationForm()
#     form.questions.choices = [(q.id, q.text) for q in Question.query.all()]
#     form.interests.choices = [(i.id, i.name) for i in Interest.query.all()]

#     if form.validate_on_submit():
#         new_exam = Exam(
#             exam_title=form.exam_title.data,
#             description=form.description.data,
#             exam_date=form.exam_date.data,
#             duration=form.duration.data,
#             created_by=current_user.id,
#             interests=",".join(map(str, form.interests.data))  # Store selected interests
#         )
#         db.session.add(new_exam)
#         db.session.commit()

#         # Clear existing associations and link selected questions to the exam
#         ExamQuestion.query.filter_by(exam_id=new_exam.id).delete()
#         for question_id in form.questions.data:
#             exam_question = ExamQuestion(exam_id=new_exam.id, question_id=question_id)
#             db.session.add(exam_question)
        
#         db.session.commit()
        
#         flash('Exam created successfully!', 'success')
#         return redirect(url_for('admin_dashboard'))

#     return render_template('exam-creation.html', form=form)

@app.route("/exam_creation", methods=['GET', 'POST'])
@login_required
def exam_creation():
    if not current_user.is_admin:
        flash('Only admins can create exams.', 'danger')
        return redirect(url_for('login'))

    form = ExamCreationForm()

    # Populate form choices
    form.interests.choices = [(i.id, i.name) for i in Interest.query.all()]
    form.questions.choices = [(q.id, q.text) for q in Question.query.all()]

    if form.validate_on_submit():
        selected_question_ids = form.questions.data
        
        new_exam = Exam(
            exam_title=form.exam_title.data,
            description=form.description.data,
            exam_date=form.exam_date.data,
            duration=form.duration.data,
            created_by=current_user.id,
            interests=",".join(map(str, form.interests.data))
        )
        
        db.session.add(new_exam)
        db.session.commit()

        # Link selected questions to the new exam
        for question_id in selected_question_ids:
            exam_question = ExamQuestion(exam_id=new_exam.id, question_id=question_id)
            db.session.add(exam_question)
        
        db.session.commit()
        
        flash('Exam created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('exam-creation.html', form=form)


@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    if current_user.is_admin:
        exams = Exam.query.all()
        return render_template('admin_dashboard.html', exams=exams)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

@app.route("/take_exam/<int:exam_id>", methods=['GET', 'POST'])
@login_required
def take_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    total_questions = len(questions)
    current_question_index = int(request.args.get('index', 0))

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        question_id = request.form.get('question_id')

        if selected_answer:
            session[f'question_{question_id}'] = selected_answer

        next_index = current_question_index + 1
        if next_index >= total_questions:
            return redirect(url_for('submit_exam', exam_id=exam_id))
        else:
            return redirect(url_for('take_exam', exam_id=exam_id, index=next_index))

    if current_question_index >= total_questions:
        return redirect(url_for('submit_exam', exam_id=exam_id))

    current_question = questions[current_question_index]
    user_selected_language = current_user.selected_language  # Assuming this is set up

    translator = Translator()
    try:
        if user_selected_language and user_selected_language != 'en':
            translated_question_text = translator.translate(current_question.text, dest=user_selected_language).text
            translated_options = [translator.translate(option, dest=user_selected_language).text for option in current_question.options]
            options_with_translations = [(option, translated_option) for option, translated_option in zip(current_question.options, translated_options)]
        else:
            translated_question_text = current_question.text
            options_with_translations = [(option, option) for option in current_question.options]
    except Exception as e:
        print(f"Translation Error: {e}")
        translated_question_text = current_question.text
        options_with_translations = [(option, option) for option in current_question.options]

    return render_template('take_exam.html', 
                           exam=exam, 
                           question=current_question, 
                           translated_question_text=translated_question_text,
                           options_with_translations=options_with_translations, 
                           index=current_question_index, 
                           total=total_questions, 
                           user_selected_language=user_selected_language)

@app.route("/enter_interests", methods=['GET', 'POST'])
@login_required
def enter_interests():
    form = InterestsForm()
    if form.validate_on_submit():
        try:
            current_user.interests = ",".join(form.interests.data)
            current_user.language = form.language.data
            current_user.selected_language = form.language.data  # Ensure this line is executed
            current_user.last_interests_update = datetime.utcnow()
            db.session.commit()
            flash('Interests updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your interests. Please try again.', 'error')
            print(f"Error: {e}")  # Log error for debugging
        return redirect(url_for('student_dashboard'))
    
    return render_template('enter_interests.html', form=form)

@app.route("/add_question", methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        if not form.text.data or not form.answer.data:
            flash('Question text and answer are required.', 'danger')
            return redirect(url_for('add_question'))

        new_question = Question(
            text=form.text.data,
            options=form.options.data,
            answer=form.answer.data,
            difficulty=form.difficulty.data
        )
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_question.html', form=form)

# @app.route("/submit_result/<int:exam_id>", methods=['POST'])
# @login_required
# def submit_result(exam_id):
#     # Get the submitted answers from the form
#     answers = request.form

#     # Fetch the exam and the student's previous answers if needed
#     exam = Exam.query.get_or_404(exam_id)
#     student_id = current_user.id

#     # Calculate score and provide feedback
#     score = 0
#     feedback = ""

#     for question_id, answer in answers.items():
#         # Validate that the answer is correct
#         question = Question.query.get(question_id)
#         if question and question.answer == answer:
#             score += 1
        
#     # Save the result
#     new_result = ExamResult(
#         exam_id=exam_id,
#         student_id=student_id,
#         score=score,
#         feedback=feedback
#     )
#     db.session.add(new_result)
#     db.session.commit()
    
#     flash('Exam submitted successfully! Your score is {}'.format(score), 'success')
#     return redirect(url_for('results'))  # Redirect to results or another relevant page

@app.route('/view_exams')
@login_required
def view_exams():
    exams = Exam.query.all()  # This fetches all exams from the database
    return render_template('view_exams.html', exams=exams)

def get_questions_for_exam(exam_id):
    """
    Fetch all questions for a given exam ID.
    """
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).all()
    questions = [eq.question for eq in exam_questions]
    return questions

# @app.route('/exam_submission', methods=['GET'])
# @login_required
# def exam_submission():
#     # Get exam_id and score from request arguments
#     exam_id = request.args.get('exam_id', type=int)
#     score = request.args.get('score', type=int)

#     # Fetch the exam and questions
#     exam = Exam.query.get_or_404(exam_id)
#     questions = Question.query.filter_by(exam_id=exam_id).all()

#     # Render template with exam details and score
#     return render_template('exam_submission.html', exam=exam, questions=questions, score=score)
@app.route('/exam_submission', methods=['GET'])
@login_required
def exam_submission():
    # Get exam_id and score from request arguments
    exam_id = request.args.get('exam_id', type=int)
    score = request.args.get('score', type=int)

    # Fetch the exam and questions
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()

    # # Render template with exam details and score
    return render_template('exam_submission.html', exam=exam, questions=questions, score=score)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# @app.route("/submit_exam/<int:exam_id>", methods=['POST'])
# @login_required
# def submit_exam(exam_id):
#     answers = {}
#     for key, value in request.form.items():
#         if key.startswith('question_'):
#             question_id = key.split('_')[1]
#             answers[question_id] = value

#     exam = Exam.query.get(exam_id)
#     if not exam:
#         flash('Exam not found!', 'error')
#         return redirect(url_for('home'))

#     # Check if all questions have been answered
#     total_questions = len(exam.questions)
#     if len(answers) != total_questions:
#         flash('Please answer all questions before submitting!', 'error')
#         return redirect(url_for('take_exam', exam_id=exam_id, index=0))  # Redirect to the first question

#     # Calculate score
#     score = sum(1 for question_id, answer in answers.items() if Question.query.get(question_id).answer == answer)

#     # Save result
#     result = ExamResult(exam_id=exam_id, student_id=current_user.id, score=score)
#     db.session.add(result)
#     db.session.commit()

#     flash('Exam submitted successfully!', 'success')
#     return redirect(url_for('results'))

# @app.route("/submit_exam/<int:exam_id>", methods=['POST','GET'])
# @login_required
# def submit_exam(exam_id):
#     answers = {}
    
#     # Collect answers from form data
#     for key, value in request.form.items():
#         if key.startswith('question_'):
#             question_id = key.split('_')[1]
#             answers[question_id] = value

#     # Get the exam object
#     exam = Exam.query.get(exam_id)
#     if not exam:
#         flash('Exam not found!', 'error')
#         return redirect(url_for('home'))

#     # Check if all questions have been answered
#     total_questions = len(exam.questions)
#     if len(answers) != total_questions:
#         flash('Please answer all questions before submitting!', 'error')
#         return redirect(url_for('take_exam', exam_id=exam_id))

#     # Calculate score based on correct answers
#     score = sum(
#         1 for question_id, answer in answers.items()
#         if Question.query.get(question_id).answer == answer
#     )

#     # Save the result to the database
#     result = ExamResult(exam_id=exam_id, student_id=current_user.id, score=score)
#     db.session.add(result)
#     db.session.commit()

#     flash('Exam submitted successfully!', 'success')
#     # Redirect to `exam_submission` route to display the score
#     return redirect(url_for('exam_submission', exam_id=exam_id, score=score))

@app.route("/submit_exam/<int:exam_id>", methods=["POST"])
@login_required
def submit_exam(exam_id):
    # Collect answers from the form
    answers = {}
    for key, value in request.form.items():
        if key.startswith("question_"):
            question_id = key.split("_")[1]
            answers[question_id] = value

    # Fetch the exam and validate
    exam = Exam.query.get_or_404(exam_id)
    total_questions = len(exam.questions)

    # Ensure all questions are answered
    if len(answers) != total_questions:
        flash("Please answer all questions before submitting!", "error")
        return redirect(url_for("take_exam", exam_id=exam_id))

    # Calculate the score
    score = sum(
        1
        for question_id, answer in answers.items()
        if Question.query.get(question_id).answer == answer
    )

    # Save the result in the database
    result = ExamResult(exam_id=exam_id, student_id=current_user.id, score=score)
    db.session.add(result)
    db.session.commit()

    # Show success message
    flash("Exam submitted successfully!", "success")

    # Render the results page
    return render_template(
        "exam_submission.html", score=score, questions=exam.questions
    )




@app.route('/update_language', methods=['POST'])
@login_required
def update_language():
    selected_language = request.form.get('language')
    if selected_language:
        current_user.selected_language = selected_language
        db.session.commit()
    return redirect(url_for('profile'))  # Redirect to a profile page or wherever appropriate

@app.route('/skip_question/<int:question_id>', methods=['POST'])
def skip_question(question_id):
    exam_id = request.cookies.get('exam_id')  # Ensure you have a way to identify the exam session
    # Add logic to track the skipped question (e.g., database record or session data)
    skipped_question = SkippedQuestion(exam_id=exam_id, question_id=question_id)
    db.session.add(skipped_question)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == "__main__":
    # if not os.path.exists(UPLOAD_FOLDER):
    #     os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)