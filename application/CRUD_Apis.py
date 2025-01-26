from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import *
from flask_restful import Resource
from application.models import *
from application.database import db
class Test(Resource):
    def get(self):
        return {"msg": "Test successful"}, 200
    @role_required('admin')
    def post(self):
        return request.json, 200
    
class Courses(Resource):
    def get(self):
        courses = Course.objects().to_json()
        return {"res":courses}, 200