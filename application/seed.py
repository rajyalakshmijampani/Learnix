import uuid
from application.models import *
from application.database import db
from werkzeug.security import generate_password_hash
import datetime
import random
import json

def seed_databases():
    print("Starting database seeding...")
    
    try:
        # Create roles
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

        # Create instructors before courses
        instructor_data = [
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com'),
            ('Robert Johnson', 'robert@example.com'),
            ('Sarah Wilson', 'sarah@example.com')
        ]

        instructor_objects = []
        for name, email in instructor_data:
            if not User.query.filter_by(email=email).first():
                instructor = User(
                    id=str(uuid.uuid4()),
                    name=name,
                    email=email,
                    password=generate_password_hash('instructor123'),
                    active=True,
                    fs_uniquifier=str(uuid.uuid4())
                )
                instructor.roles.append(role_objects['instructor'])
                db.session.add(instructor)
                instructor_objects.append(instructor)
        
        db.session.commit()

        # Create admin
        admin_email = 'admin@example.com'
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                id=str(uuid.uuid4()),
                name='Admin User',
                email=admin_email,
                password=generate_password_hash('admin123'),
                active=True,
                fs_uniquifier=str(uuid.uuid4())
            )
            admin.roles.append(role_objects['admin'])
            db.session.add(admin)

        # Create students
        students_data = [
            ('Alice Johnson', 'alice@example.com'),
            ('Bob Smith', 'bob@example.com'),
            ('Carol White', 'carol@example.com')
        ]

        student_objects = []
        for name, email in students_data:
            if not User.query.filter_by(email=email).first():
                student = User(
                    id=str(uuid.uuid4()),
                    name=name,
                    email=email,
                    password=generate_password_hash('student123'),
                    active=True,
                    fs_uniquifier=str(uuid.uuid4())
                )
                student.roles.append(role_objects['student'])
                db.session.add(student)
                student_objects.append(student)

        # Create courses and related data
        course_data = [
            ("Introduction to Python", "Learn Python programming from scratch.", "Programming"),
            ("Data Structures & Algorithms", "Master fundamental data structures and algorithms.", "Computer Science"),
            ("Web Development Fundamentals", "Learn modern web development.", "Web Development")
        ]

        course_objects = []
        for idx, (title, description, category) in enumerate(course_data):
            if not Course.query.filter_by(title=title).first():
                course = Course(
                    id=str(uuid.uuid4()),
                    title=title,
                    description=description,
                    category=category
                )
                # Assign 2 instructors to each course (rotating through the instructor list)
                course.instructors.extend([
                    instructor_objects[idx % len(instructor_objects)],
                    instructor_objects[(idx + 1) % len(instructor_objects)]
                ])
                db.session.add(course)
                course_objects.append(course)
                
                # Create weeks for each course
                for week_num in range(1, 5):  # 4 weeks of content
                    week = Week(
                        id=str(uuid.uuid4()),
                        week_number=week_num,
                        course_id=course.id
                    )
                    db.session.add(week)
                    
                    # Add videos
                    for vid_num in range(1, 3):
                        video = Video(
                            id=str(uuid.uuid4()),
                            title=f"{title} - Week {week_num} Video {vid_num}",
                            url=f"http://example.com/video{vid_num}",
                            transcript=f"Transcript {week_num}_{vid_num}",
                            duration=600,
                            week_id=week.id
                        )
                        db.session.add(video)
                    
                    # Add assignments
                    for assignment_type in ['graded', 'practice']:
                        assignment = Assignment(
                            id=str(uuid.uuid4()),
                            type=assignment_type,
                            week_id=week.id
                        )
                        db.session.add(assignment)
                        
                        # Add questions with random correct answers
                        for q_num in range(1, 11):
                            correct_option = random.randint(0, 3)  # Random correct answer
                            question = Question(
                                id=str(uuid.uuid4()),
                                question=f"{title} - Week {week_num} Question {q_num}",
                                options=json.dumps([
                                    f"Option A for Q{q_num}", 
                                    f"Option B for Q{q_num}", 
                                    f"Option C for Q{q_num}", 
                                    f"Option D for Q{q_num}"
                                ]),
                                correct_option=correct_option,
                                assignment_id=assignment.id
                            )
                            db.session.add(question)

        db.session.commit()

        # Subscribe students to courses and add week 1 progress
        for student in student_objects:
            # Subscribe to first two courses
            for course in course_objects[:2]:
                # Create course progress
                course_progress = CourseProgress(
                    id=str(uuid.uuid4()),
                    student_id=student.id,
                    course_id=course.id
                )
                db.session.add(course_progress)

                # Add week 1 progress
                week = Week.query.filter_by(course_id=course.id, week_number=1).first()
                
                # Video progress
                for video in week.videos:
                    video_progress = VideoProgress(
                        id=str(uuid.uuid4()),
                        video_id=video.id,
                        student_id=student.id,
                        status='completed'
                    )
                    db.session.add(video_progress)

                # Assignment progress with random scores
                for assignment in week.assignments:
                    score = random.randint(6, 10)  # Random score between 6 and 10
                    marked_options = [random.randint(0, 3) for _ in range(10)]  # Random answers
                    progress = AssignmentProgress(
                        id=str(uuid.uuid4()),
                        assignment_id=assignment.id,
                        student_id=student.id,
                        score=score,
                        max_score=10,
                        marked_options=json.dumps(marked_options)
                    )
                    db.session.add(progress)

        db.session.commit()
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.session.rollback()
        raise e

