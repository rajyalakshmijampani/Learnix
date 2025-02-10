import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from application.database import db
from application.Auth_Apis import UserRegistration, UserLogin, ProtectedResource, AssignRole, RoleList
from application.models import User, Role
from werkzeug.security import generate_password_hash
from application.CRUD_Apis import *
from application.seed import seed_databases
from application.Gen_Ai import CourseAssistant,GenerateQuestions

def create_app():
    app = Flask(__name__)

    # Load the config from config.py inside the applications folder
    app.config.from_object('application.config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app)

    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()
        seed_databases()

    # Add Auth resources to the API
    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(ProtectedResource, '/protected')
    api.add_resource(AssignRole, '/assign-role')
    api.add_resource(RoleList, '/roles')
    # Add CRUD resources to the API
    api.add_resource(Test, '/test')
    api.add_resource(Courses, '/courses')
    api.add_resource(StudentById, '/students/<string:student_id>')
    api.add_resource(CourseById, '/courses/<string:course_id>')
    # Add Gen AI resources to the API
    api.add_resource(CourseAssistant, '/chat/course')
    api.add_resource(GenerateQuestions, "/generate-mcqs")



    return app
