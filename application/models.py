from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from .database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps


def role_required(role):
    """
    Custom decorator to ensure the user is authenticated with JWT and has the required role.
    """
    def decorator(fn):
        @jwt_required()  # This ensures that JWT is required for all routes using this decorator
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get current user's identity from the JWT token
            current_user_id = get_jwt_identity()

            # Retrieve the user from the database
            user = User.query.get(current_user_id)
            if not user:
                return {"msg": "User not found"}, 404

            # Check if the user has the required role
            if role not in [r.name for r in user.roles]:
                return {"msg": "User does not have required role"}, 403

            # Proceed to the original function
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(25),nullable=False)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String,nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255),unique=True,nullable=False)
    roles = db.relationship('Role',secondary='roles_users',
                            backref = db.backref('users',lazy='dynamic'))

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String,unique=True)
    description = db.Column(db.String(255))

class RolesUsers(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column('user_id',db.Integer(),db.ForeignKey('user.id'))
    role_id = db.Column('role_id',db.Integer(),db.ForeignKey('role.id'))

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lectureNumber = db.Column(db.Float, nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    weekNumber = db.Column(db.Integer, nullable=False)

