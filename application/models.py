from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from .database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from mongoengine import (
    Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField,
    IntField, FloatField, BooleanField, DictField, DateTimeField, ReferenceField
)
import datetime


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

# Embedded document for video content
class Video(EmbeddedDocument):
    video_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    url = StringField(required=True)
    transcript = StringField()
    duration = IntField(min_value=0)


# Embedded document for questions in assignments
class Question(EmbeddedDocument):
    question = StringField(required=True)
    options = ListField(StringField(), required=True)
    correct_option = IntField(required=True)


# Embedded document for assignments
class Assignment(EmbeddedDocument):
    assignment_id = StringField(required=True, unique=True)
    questions = ListField(EmbeddedDocumentField(Question), required=True)


# Embedded document for weekly content
class WeeklyContent(EmbeddedDocument):
    videos = ListField(EmbeddedDocumentField(Video), required=True)
    graded_assignments = ListField(EmbeddedDocumentField(Assignment))
    practice_assignments = ListField(EmbeddedDocumentField(Assignment))


# Main document for Course
class Course(Document):
    title = StringField(required=True, max_length=255)
    description = StringField(required=True)
    category = StringField(required=True, max_length=100)
    instructors = ListField(StringField(), required=True)  # List of instructor IDs
    weeks = DictField(field=EmbeddedDocumentField(WeeklyContent))
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)


# Embedded document for video progress
class VideoProgress(EmbeddedDocument):
    video_id = StringField(required=True)
    status = StringField(choices=["not_started", "in_progress", "completed"], required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)


# Embedded document for assignment progress
class AssignmentProgress(EmbeddedDocument):
    assignment_id = StringField(required=True)
    score = IntField(min_value=0, required=True)
    max_score = IntField(min_value=0, required=True)


# Embedded document for weekly progress
class WeeklyProgress(EmbeddedDocument):
    videos = ListField(EmbeddedDocumentField(VideoProgress), required=True)
    graded_assignments = ListField(EmbeddedDocumentField(AssignmentProgress))
    practice_assignments = ListField(EmbeddedDocumentField(AssignmentProgress))

# Embedded document for course progress
class CourseProgress(EmbeddedDocument):
    course_id = StringField(required=True)  # Reference to Course ID
    weekly_progress = DictField(field=EmbeddedDocumentField(WeeklyProgress), required=True)

# Main Student document
class Student(Document):
    name = StringField(required=True, max_length=255)
    email = StringField(required=True, unique=True)
    course_progress = ListField(EmbeddedDocumentField(CourseProgress), required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
