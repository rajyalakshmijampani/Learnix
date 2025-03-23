from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from application.config import Config
from flask_security import SQLAlchemyUserDatastore
import os
import pickle

base_dir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(base_dir, '..','..','frontend', 'templates')
static_folder = os.path.join(base_dir,'..','..','frontend', 'static')


faiss_cache = {}

def load_faiss_for_week(week):
    if week in faiss_cache:
        return faiss_cache[week]
    
    faiss_folder = os.path.join(base_dir,'..', 'FAISS')
    faiss_index_path = os.path.join(faiss_folder, f"faiss_index_week{week}.pkl")

    if not os.path.exists(faiss_index_path):
        print(f"FAISS index for Week {week} not found.")
        return None

    with open(faiss_index_path, "rb") as f:
        faiss_cache[week] = pickle.load(f)
        
    return faiss_cache[week]    

app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)

# Initialize models after app context is created
from application.models import User,Role,Lecture,Course

def create_datastore():
    # Initialize datastore after the app context
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    return datastore

with app.app_context():

    db.create_all()

    datastore  = create_datastore()
    datastore.find_or_create_role(name='admin',description='Admin role')
    datastore.find_or_create_role(name='user',description='User role')
    
#     if not datastore.find_user(email='admin@email.com'):
#         datastore.create_user(email='admin@email.com',password=generate_password_hash('admin'),name='admin',roles=['admin'])
    
    default_courses = ["Business Analytics", "Software Engineering", "Software Testing", "Deep Learning"]

    for course_name in default_courses:
        course = Course.query.filter_by(name=course_name).first() # Check duplicates
        if not course:
            new_course = Course(name=course_name)
            db.session.add(new_course)
            db.session.commit() # Commit to get the course ID
        
            # Insert default lectures for the new course
            if new_course.name == 'Business Analytics':
                default_lectures = [
                    {'course_id': new_course.id, 'lectureNumber': '1.1', 'title': 'Introduction to Data Visualization', 'link': 'https://youtu.be/_0z2c-Awpt0', 'weekNumber': 1},
                    {'course_id': new_course.id, 'lectureNumber': '1.2', 'title': 'Defining the Message', 'link': 'https://youtu.be/1zWJyhv6j_g', 'weekNumber': 1},
                    {'course_id': new_course.id, 'lectureNumber': '1.3', 'title': 'Creating Designs', 'link': 'https://youtu.be/lLvRWjclPus', 'weekNumber': 1},
                    {'course_id': new_course.id, 'lectureNumber': '2.1', 'title': 'Probability Distributions', 'link': 'https://youtu.be/yMFsKaMRqdw', 'weekNumber': 2},
                    {'course_id': new_course.id, 'lectureNumber': '2.2', 'title': 'Business Example', 'link': 'https://youtu.be/ePqGFuLnVFM', 'weekNumber': 2},
                    {'course_id': new_course.id, 'lectureNumber': '2.3', 'title': 'Guessing the Distribution', 'link': 'https://youtu.be/UM-3E8fsCgA', 'weekNumber': 2},
                    {'course_id': new_course.id, 'lectureNumber': '3.1', 'title': 'Determining Association Between Categorical Variables', 'link': 'https://youtu.be/wWFK-N7RTKU', 'weekNumber': 3}
                ]

                for lecture_data in default_lectures:
                    lecture = Lecture.query.filter_by(course_id=lecture_data['course_id'], lectureNumber=lecture_data['lectureNumber']).first()
                    if not lecture:
                        new_lecture = Lecture(
                                                course_id=lecture_data['course_id'],
                                                lectureNumber=lecture_data['lectureNumber'],
                                                title=lecture_data['title'],
                                                link=lecture_data['link'],
                                                weekNumber=lecture_data['weekNumber']
                                            )
                        db.session.add(new_lecture)

    db.session.commit()

    weeks = {lecture.weekNumber for lecture in Lecture.query.distinct(Lecture.weekNumber).all()}
    faiss_store = {week: load_faiss_for_week(week) for week in weeks}



# Import the controllers after app context is set up
from . import controllers