from flask import current_app as app,jsonify,request,render_template,Response,send_file,redirect
from flask_security import auth_required, roles_required,current_user
from flask_restful import marshal,fields
from .models import db,User,Role,Lecture
from .datastore import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime,timedelta
from sqlalchemy import and_,func

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
    return jsonify({"message":"User registered successfully"})