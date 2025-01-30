from flask import current_app as app,jsonify,request,render_template,Response,redirect
from flask_security import auth_required, roles_required,current_user
from flask_restful import marshal,fields
from .models import db,User,Role,Course,Registration,Lecture
from .datastore import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select

course_fields = {
    "id": fields.Integer,
    "name": fields.String
    }

@app.get('/login')
def login():
    print("Redirecting to /#/")
    return redirect('/#/')

@app.get('/')
def home():
    return render_template("index.html")

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "name": fields.String
    }

@app.post('/register')
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body required"}),400

    name=data.get('name')
    email = data.get('email')
    password = data.get("password")
    if not name:
        return jsonify({"message":"Name is required"}),400
    if not email:
        return jsonify({"message":"Email is required"}),400
    if not password :
        return jsonify({"message":"Password is required"}),400
    user = datastore.find_user(email=email)
    if user:
        return jsonify({"message":"Email already exists"}),404
    user = datastore.create_user(name=name,email=email,password=generate_password_hash(password),roles=['user'])
    db.session.commit()

    # Register for default courses
    available_courses = Course.query.with_entities(Course.id).all()  # Fetch all course IDs
    registrations = [Registration(user_id=user.id, course_id=course.id) for course in available_courses]
    db.session.bulk_save_objects(registrations)  # Bulk insert for efficiency
    db.session.commit()

    return jsonify({"message":"User registered successfully"})

@app.post('/user_login')
def user_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body required"}),400

    email = data.get('email')
    password = data.get("password")
    if not email:
        return jsonify({"message":"Email is required"}),400
    if not password :
        return jsonify({"message":"Password is required"}),400
    user = datastore.find_user(email=email)
    if not user:
        return jsonify({"message":"User not found"}),404
    if check_password_hash(user.password,password):
        marshalled_data = marshal(user, user_fields)
        return jsonify({**marshalled_data, **{"role":user.roles[0].name,"token":user.get_auth_token()}})
    else:
        return jsonify({"message":"Incorrect password"}),400
    
@app.get('/user/<int:user_id>/currentcourses')
def get_user_currentcourses(user_id):
    registered_subquery = select(Registration.course_id).where(Registration.user_id == user_id)
    registered_courses = Course.query.with_entities(Course.id,Course.name).filter(Course.id.in_(registered_subquery)).all()
    result = [{"id": course[0], "name": course[1]} for course in registered_courses]
    return jsonify(result)

@app.get('/get_all_lectures/<int:id>')
def get_all_lectures(id):
    lectures =Lecture.query.filter_by(course_id=id).all()
    lectures_data = []
    for lecture in lectures:
        lectures_data.append({
            'lecturenumber': lecture.lectureNumber,
            'title': lecture.title,
            'link':lecture.link,
            'weeknumber': lecture.weekNumber,
        })
    return jsonify(lectures_data)