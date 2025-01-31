from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import *
from flask_restful import Resource
from application.models import *
from application.database import db
from bson import json_util
import uuid
import datetime

class Test(Resource):
    def get(self):
        return {"msg": "Test successful"}, 200
    @role_required('admin')
    def post(self):
        return request.json, 200
    
class Courses(Resource):
    def get(self):
        page = int(request.args.get("page", 1))  # Default to page 1
        limit = 10  # Number of results per page
        skip_count = (page - 1) * limit

        courses = Course.objects().skip(skip_count).limit(limit)
        courses_list = [course.to_dict() for course in courses]

        return {
            "res": courses_list,
            "page": page,
            "has_more": Course.objects().count() > skip_count + limit  # Check if there's a next page
        }, 200

class StudentById(Resource):
    def get(self, student_id):
        try:
            student = Student.objects(id=uuid.UUID(student_id)).first()
            if not student:
                return {"msg": "Student not found"}, 404
            
            # Use the to_dict method which properly handles datetime serialization
            return student.to_dict(), 200
            
        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}, 500

    def put(self, student_id):
        try:
            student = Student.objects(id=uuid.UUID(student_id)).first()
            if not student:
                return {"msg": "Student not found"}, 404

            data = request.json
            allowed_fields = ['name', 'email', 'course_progress']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.datetime.utcnow()

            # Use modify instead of update for better control
            student.modify(**update_data)
            student.reload()

            return student.to_dict(), 200

        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            return {"msg": f"Error updating student: {str(e)}"}, 500

class CourseById(Resource):
    def get(self, course_id):
        try:
            course = Course.objects(id=uuid.UUID(course_id)).first()
            if not course:
                return {"msg": "Course not found"}, 404
            return course.to_dict(), 200
        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}, 500

    def put(self, course_id):
        try:
            course = Course.objects(id=uuid.UUID(course_id)).first()
            if not course:
                return {"msg": "Course not found"}, 404

            data = request.json
            allowed_fields = ['title', 'description', 'category', 'instructors', 'weeks']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.datetime.utcnow()

            # Use modify instead of update for better control
            course.modify(**update_data)
            course.reload()

            return course.to_dict(), 200

        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            return {"msg": f"Error updating course: {str(e)}"}, 500



