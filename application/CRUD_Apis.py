from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import *
from flask_restful import Resource
from application.models import *
from application.database import db
from bson import json_util
import uuid
import datetime
import json  # Add this import

class Test(Resource):
    def get(self):
        return {"msg": "Test successful"}, 200
    @role_required('admin')
    def post(self):
        return request.json, 200
    
class Courses(Resource):
    def get(self):
        page = int(request.args.get("page", 1))
        per_page = 10
        
        courses = Course.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            "res": [self.course_to_dict(course) for course in courses.items],
            "page": page,
            "has_more": courses.has_next
        }, 200
    
    def course_to_dict(self, course):
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "created_at": str(course.created_at),
            "updated_at": str(course.updated_at),
            "instructors": [{
                "id": instructor.id,
                "name": instructor.name
            } for instructor in course.instructors]
        }

class StudentById(Resource):
    def get(self, student_id):
        try:
            student = User.query.filter_by(id=student_id).first()
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
            student = User.query.filter_by(id=student_id).first()
            if not student:
                return {"msg": "Student not found"}, 404

            data = request.json
            allowed_fields = ['name', 'email', 'course_progress']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.datetime.utcnow()

            # Use modify instead of update for better control
            for field in allowed_fields:
                if field in data:
                    setattr(student, field, data[field])
            
            student.updated_at = datetime.datetime.utcnow()
            db.session.commit()

            return student.to_dict(), 200

        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating student: {str(e)}"}, 500

class CourseById(Resource):
    def get(self, course_id):
        try:
            course = Course.query.filter_by(id=course_id).first()
            if not course:
                return {"msg": "Course not found"}, 404
            
            return self.course_to_dict(course), 200
        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}, 500

    def put(self, course_id):
        try:
            course = Course.query.filter_by(id=course_id).first()
            if not course:
                return {"msg": "Course not found"}, 404

            data = request.json
            allowed_fields = ['title', 'description', 'category']
            
            for field in allowed_fields:
                if field in data:
                    setattr(course, field, data[field])
            
            course.updated_at = datetime.datetime.utcnow()
            db.session.commit()

            return self.course_to_dict(course), 200

        except ValueError:
            return {"msg": "Invalid UUID format"}, 400
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating course: {str(e)}"}, 500
    
    def course_to_dict(self, course):
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "category": course.category,
            "created_at": str(course.created_at),
            "updated_at": str(course.updated_at),
            "instructors": [{
                "id": instructor.id,
                "name": instructor.name
            } for instructor in course.instructors],
            "weeks": [{
                "id": week.id,
                "week_number": week.week_number,
                "videos": [{
                    "id": video.id,
                    "title": video.title,
                    "url": video.url,
                    "duration": video.duration
                } for video in week.videos],
                "assignments": [{
                    "id": assignment.id,
                    "type": assignment.type,
                    "questions": [{
                        "id": question.id,
                        "question": question.question,
                        "options": json.loads(question.options) if question.options else []
                    } for question in assignment.questions]
                } for assignment in week.assignments]
            } for week in course.weeks]
        }

class StudentProgress(Resource):
    # @jwt_required()
    def get(self, student_id):
        student = User.query.get_or_404(student_id)
        progress = CourseProgress.query.filter_by(student_id=student_id).all()
        return {
            "id": student_id,
            "name": student.name,
            "email": student.email,
            "course_progress": [p.to_dict() for p in progress]
        }, 200

class StudentAssignmentProgress(Resource):
    # @jwt_required()
    def get(self, student_id, course_id, week_number, assignment_type):
        try:
            # Verify assignment type
            if assignment_type not in ['graded', 'practice']:
                return {"msg": "Invalid assignment type. Must be 'graded' or 'practice'"}, 400

            # Get the week
            week = Week.query.filter_by(
                course_id=course_id,
                week_number=week_number
            ).first()
            if not week:
                return {"msg": "Week not found"}, 404

            # Get assignment for the week and type
            assignment = Assignment.query.filter_by(
                week_id=week.id,
                type=assignment_type
            ).first()
            if not assignment:
                return {"msg": "Assignment not found"}, 404

            # Get student's progress for this assignment
            progress = AssignmentProgress.query.filter_by(
                student_id=student_id,
                assignment_id=assignment.id
            ).first()

            if not progress:
                return {
                    "msg": "No progress found for this assignment",
                    "assignment_id": assignment.id,
                    "completed": False
                }, 200

            # Get questions with student's answers
            questions = Question.query.filter_by(assignment_id=assignment.id).all()
            marked_options = json.loads(progress.marked_options) if progress.marked_options else []

            return {
                "assignment_id": assignment.id,
                "completed": True,
                "score": progress.score,
                "max_score": progress.max_score,
                "questions": [{
                    "id": q.id,
                    "question": q.question,
                    "options": json.loads(q.options) if q.options else [],
                    "marked_option": marked_options[i] if i < len(marked_options) else None,
                    "correct_option": q.correct_option if assignment_type == 'practice' else None  # Only show correct answers for practice
                } for i, q in enumerate(questions)]
            }, 200

        except Exception as e:
            return {"msg": f"Error: {str(e)}"}, 500

class StudentVideoProgress(Resource):
    # @jwt_required()
    def get(self, student_id, course_id, week_number):
        try:
            # Get the week
            week = Week.query.filter_by(
                course_id=course_id,
                week_number=week_number
            ).first()
            if not week:
                return {"msg": "Week not found"}, 404

            # Get all videos for the week
            videos = Video.query.filter_by(week_id=week.id).all()
            
            # Get progress for each video
            video_progress = []
            for video in videos:
                progress = VideoProgress.query.filter_by(
                    student_id=student_id,
                    video_id=video.id
                ).first()

                video_progress.append({
                    "video_id": video.id,
                    "title": video.title,
                    "url": video.url,
                    "duration": video.duration,
                    "status": progress.status if progress else "not_started",
                    "last_watched": str(progress.timestamp) if progress else None
                })

            return {
                "week_number": week_number,
                "course_id": course_id,
                "videos": video_progress
            }, 200

        except Exception as e:
            return {"msg": f"Error: {str(e)}"}, 500



