from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import *
from flask_restful import Resource
from application.models import *
from application.database import db
from bson import json_util

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
        student = Student.objects(id=student_id).first()
        if not student:
            return {"msg": "Student not found"}, 404
        return student.to_mongo().to_dict(), 200

class CourseById(Resource):
    def get(self, course_id):
        course = Course.objects(id=course_id).first()
        if not course:
            return {"msg": "Course not found"}, 404
        return course.to_dict(), 200
    # @role_required('admin')
    def put(self, course_id):
        course = Course.objects(id=course_id).first()
        if not course:
            return {"msg": "Course not found"}, 404

        data = request.json
        course.update(**data)
        course.reload()
        return course.to_dict(), 200



