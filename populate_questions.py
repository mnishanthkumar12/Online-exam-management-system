from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for,session
from one import Question,Interest
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/examdb"
app.config['SECRET_KEY']='d1aef0865aaaaec841dabcafdeac22aa53b8ebcd4610436c56dd6d105c2561492e8b232b445dac92548e8d59ad0871ed9f'
db=SQLAlchemy(app)

questions = [
    {"text": "What is the study of plants called?", "options": ["Botany", "Zoology", "Geology", "Astronomy"], "answer": "Botany", "difficulty": "medium"},
    {"text": "What element is diamond made of?", "options": ["Carbon", "Silicon", "Nitrogen", "Oxygen"], "answer": "Carbon", "difficulty": "hard"}
]

def populate_questions(exam_id):
    with app.app_context():
        for q in questions:
            question = Question(
                text=q['text'],
                exam_id=exam_id,
                options=q['options'],
                answer=q['answer'],
                difficulty=q['difficulty']
            )
            db.session.add(question)
        db.session.commit()
        print("Questions have been added to the database.")

interests = [
    {"name": "Mathematics"},
    {"name": "Science"},
    {"name": "History"}
]

def populate_interests():
    with app.app_context():
        for i in interests:
            interest = Interest(name=i['name'])
            db.session.add(interest)
        db.session.commit()
        print("Interests have been added to the database.")

if __name__ == "__main__":
    populate_questions(17)
    populate_interests()