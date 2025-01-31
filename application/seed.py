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
            ('Carol White', 'carol@example.com'),
            ('David Brown', 'david@example.com')
        ]
        
        student_docs = []
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
                    student_doc = Student(
                        id=student_id,
                        name=name,
                        email=email,
                        course_progress=[]
                    )
                    student_doc.save()
                    student_docs.append(student_doc)

        db.session.commit()

        # Create courses in MongoDB if not exists
        courses = [
            ("Introduction to Python", "Learn Python programming from scratch.", "Programming"),
            ("Data Structures & Algorithms", "Master fundamental data structures and algorithms.", "Computer Science")
        ]
        
        course_docs = []
        for title, description, category in courses:
            if not Course.objects(title=title).first():
                course = Course(
                    id=uuid.uuid4(),
                    title=title,
                    description=description,
                    category=category,
                    instructors=instructor_docs[:2],  # Assign first two instructors
                    weeks={
                        f"week_{i+1}": WeeklyContent(
                            videos=[
                                Video(video_id=str(uuid.uuid4()), title=f"{title} - Week {i+1} Video 1", url="http://example.com/video1", transcript=f"Transcript {i+1}", duration=600),
                                Video(video_id=str(uuid.uuid4()), title=f"{title} - Week {i+1} Video 2", url="http://example.com/video2", transcript=f"Transcript {i+1}", duration=700)
                            ],
                            graded_assignments=[
                                Assignment(assignment_id=str(uuid.uuid4()), questions=[
                                    Question(question=f"{title} - Week {i+1} Question {j+1}", options=["Option A", "Option B"], correct_option=0)
                                    for j in range(10)
                                ])
                            ],
                            practice_assignments=[
                                Assignment(assignment_id=str(uuid.uuid4()), questions=[
                                    Question(question=f"{title} - Week {i+1} Practice Question {j+1}", options=["Option A", "Option B"], correct_option=0)
                                    for j in range(10)
                                ])
                            ]
                        ) for i in range(4)
                    }
                )
                course.save()
                course_docs.append(course)

        # Subscribe students to two courses and add progress for one week
        for student in student_docs[:2]:
            progress = []
            for course in course_docs[:2]:
                progress.append(CourseProgress(
                    course_id=str(course.id),
                    weekly_progress={
                        "week_1": WeeklyProgress(
                            videos=[VideoProgress(video_id=video.video_id, status="completed") for video in course.weeks["week_1"].videos],
                            graded_assignments=[AssignmentProgress(assignment_id=assignment.assignment_id, score=8, max_score=10, marked_options=[0]*10) for assignment in course.weeks["week_1"].graded_assignments],
                            practice_assignments=[AssignmentProgress(assignment_id=assignment.assignment_id, score=10, max_score=10, marked_options=[2]*10) for assignment in course.weeks["week_1"].practice_assignments]
                        )
                    }
                ))
            student.course_progress = progress
            student.save()

        print("Database seeding completed!")
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.session.rollback()
        raise e
