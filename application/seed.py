from mongoengine import connect
from application.models import *
from application.database import db
from werkzeug.security import generate_password_hash
import datetime
import uuid

def seed_databases():
    print("Starting database seeding...")
    
    try:
        # Connect to MongoDB
        connect('my_database', host='localhost', port=27017)
        
        # First create roles in SQLite if they don't exist
        roles = {
            'admin': 'Administrator role',
            'instructor': 'Instructor role',
            'student': 'Student role'
        }
        
        role_objects = {}
        for role_name, description in roles.items():
            existing_role = Role.query.filter_by(name=role_name).first()
            if not existing_role:
                role = Role(name=role_name, description=description)
                db.session.add(role)
                role_objects[role_name] = role
            else:
                role_objects[role_name] = existing_role
        
        db.session.commit()
        print("Roles created successfully!")

        # Clear any existing session
        db.session.remove()
        
        # Create admin if not exists
        admin_email = 'admin@example.com'
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin_id = str(uuid.uuid4())
            admin = User(
                id=admin_id,
                name='Admin User',
                email=admin_email,
                password=generate_password_hash('admin123'),
                active=True,
                fs_uniquifier=str(uuid.uuid4())
            )
            admin.roles.append(role_objects['admin'])
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")

        # Create instructors
        instructor_data = [
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com'),
            ('Bob Wilson', 'bob@example.com')
        ]
        
        instructor_docs = []
        for name, email in instructor_data:
            if not User.query.filter_by(email=email).first():
                instructor_id = str(uuid.uuid4())
                instructor = User(
                    id=instructor_id,
                    name=name,
                    email=email,
                    password=generate_password_hash('instructor123'),
                    active=True,
                    fs_uniquifier=str(uuid.uuid4())
                )
                instructor.roles.append(role_objects['instructor'])
                db.session.add(instructor)
                instructor_docs.append(Instructor(instructor_id=instructor_id, name=name))

        # Create students
        student_data = [
            ('Alice Johnson', 'alice@example.com'),
            ('Bob Smith', 'bobs@example.com'),
            ('Carol White', 'carol@example.com')
        ]
        
        for name, email in student_data:
            if not User.query.filter_by(email=email).first():
                student_id = str(uuid.uuid4())
                student = User(
                    id=student_id,
                    name=name,
                    email=email,
                    password=generate_password_hash('student123'),
                    active=True,
                    fs_uniquifier=str(uuid.uuid4())
                )
                student.roles.append(role_objects['student'])
                db.session.add(student)

                # Create MongoDB student document if not exists
                if not Student.objects(email=email).first():
                    Student(
                        id=student_id,
                        name=name,
                        email=email
                    ).save()

        db.session.commit()

        # Create course in MongoDB if not exists
        if not Course.objects(title="Introduction to Python").first():
            course_1 = Course(
                id=uuid.uuid4(),
                title="Introduction to Python",
                description="Learn Python programming from scratch.",
                category="Programming",
                instructors=instructor_docs[:2],  # First two instructors
                weeks={
                    "week_1": WeeklyContent(
                        videos=[
                            Video(video_id=str(uuid.uuid4()), title="Intro to Python", 
                                 url="http://example.com/video1", transcript="Transcript 1", duration=600)
                        ],
                        graded_assignments=[
                            Assignment(assignment_id=str(uuid.uuid4()), questions=[
                                Question(question="What is Python?", 
                                       options=["Language", "Animal"], 
                                       correct_option=0)
                            ])
                        ]
                    )
                }
            )
            course_1.save()

    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.session.rollback()
        raise e

    print("Database seeding completed!")

