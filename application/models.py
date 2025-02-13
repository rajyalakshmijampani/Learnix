from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from .database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from sqlalchemy.dialects.postgresql import JSON
import datetime
import uuid
from bson import json_util
import json


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


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True)  # Changed to String to store UUID
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hash
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                          backref=db.backref('users', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'active': self.active,
            'roles': [role.name for role in self.roles],
            'course_progress': [progress.to_dict() for progress in CourseProgress.query.filter_by(student_id=self.id).all()]
        }

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String,unique=True)
    description = db.Column(db.String(255))

class RolesUsers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.String(36), db.ForeignKey('user.id'))  # Changed to String
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Video(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    transcript = db.Column(db.Text)
    duration = db.Column(db.Integer)
    week_id = db.Column(db.String(36), db.ForeignKey('week.id'))


class Question(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(JSON)  # Stored as JSON array
    correct_option = db.Column(db.Integer, nullable=False)
    assignment_id = db.Column(db.String(36), db.ForeignKey('assignment.id'))

class Assignment(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(20))  # 'graded' or 'practice'
    week_id = db.Column(db.String(36), db.ForeignKey('week.id'))
    questions = db.relationship('Question', backref='assignment', lazy=True)

class Week(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'))
    videos = db.relationship('Video', backref='week', lazy=True)
    assignments = db.relationship('Assignment', backref='week', lazy=True)

class Course(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    weeks = db.relationship('Week', backref='course', lazy=True)
    instructors = db.relationship('User', 
                                secondary='course_instructors',
                                backref=db.backref('courses_teaching', lazy=True))

class CourseInstructors(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column('course_id', db.String(36), db.ForeignKey('course.id'))
    instructor_id = db.Column('instructor_id', db.String(36), db.ForeignKey('user.id'))

class VideoProgress(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    video_id = db.Column(db.String(36), db.ForeignKey('video.id'))
    student_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    status = db.Column(db.String(20))  # 'not_started', 'in_progress', 'completed'
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class AssignmentProgress(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    assignment_id = db.Column(db.String(36), db.ForeignKey('assignment.id'))
    student_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    marked_options = db.Column(JSON)  # Stored as JSON array

    def to_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'score': self.score,
            'max_score': self.max_score,
            'marked_options': self.marked_options
        }

class CourseProgress(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    student_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    course_id = db.Column(db.String(36), db.ForeignKey('course.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'student_id': self.student_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }