from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, IntegerField, SelectField, SubmitField,BooleanField,SelectMultipleField,TimeField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin')], validators=[DataRequired()])
    cookie = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ExamCreationForm(FlaskForm):
    exam_title = StringField('Exam Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    exam_date = DateField('Exam Date', format='%Y-%m-%d', validators=[DataRequired()])
    duration = StringField('Duration (in minutes)', validators=[DataRequired()])
    interests = SelectMultipleField('Interests')
    questions = SelectMultipleField('Questions')
    submit = SubmitField('Create Exam')
    
class QuestionForm(FlaskForm):
    text = StringField('Question Text', validators=[DataRequired()])
    options = TextAreaField('Options (comma-separated)', validators=[DataRequired()])
    answer = StringField('Correct Answer', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], validators=[DataRequired()])
    submit = SubmitField('Add Question')

class InterestsForm(FlaskForm):
    interests = SelectMultipleField(
        'Interests',
        choices=[
            ('tech', 'Technology'),
            ('sports', 'Sports'),
            ('music', 'Music'),
            ('art', 'Art'),
            ('literature', 'Literature'),
            ('science', 'Science'),
            ('history', 'History'),
            ('gaming', 'Gaming'),
            ('travel', 'Travel'),
            ('cooking', 'Cooking'),
            ('fitness', 'Fitness'),
            ('politics', 'Politics'),
            ('nature', 'Nature'),
            ('movies', 'Movies'),
            ('mathematics', 'Mathematics'),
            ('nisha', 'Nisha'),
        ],
        coerce=str
    )
    language = SelectField('Preferred Language', choices=[('English'), ('Hindi'),('Telugu')])
    submit = SubmitField('Submit Interests')


class ExamResultForm(FlaskForm):
    # Use HiddenField to store ID if you do not want them visible in the form
    exam_id = HiddenField('Exam ID', validators=[DataRequired()])
    student_id = HiddenField('Student ID', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    feedback = StringField('Feedback')
    submit = SubmitField('Submit')

