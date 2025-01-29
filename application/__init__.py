import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from application.database import db
from application.Auth_Apis import UserRegistration, UserLogin, ProtectedResource, AssignRole, RoleList
from application.models import User, Role
from werkzeug.security import generate_password_hash
from application.CRUD_Apis import *
from application.seed import seed_database
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

        # Check if the admin role exists, if not, create it
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator role')
            db.session.add(admin_role)
            db.session.commit()

        # Check if the default admin user exists, if not, create it
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            hashed_password = generate_password_hash('adminpassword')  # Set a default password
            admin_user = User(
                name='Admin',
                email='admin@example.com',
                password=hashed_password,
                active=True,
                fs_uniquifier='admin-uniquifier',
            )
            db.session.add(admin_user)
            db.session.commit()

            # Assign the admin role to the new admin user
            admin_user.roles.append(admin_role)
            db.session.commit()
    seed_database()

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

    return app
