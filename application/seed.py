from mongoengine import connect
from application.models import Course, Student, WeeklyContent, Video, Assignment, Question, VideoProgress, AssignmentProgress, WeeklyProgress, CourseProgress
import datetime

# Connect to MongoDB
connect('my_database', host='localhost', port=27017)

def seed_database():
    # Check if courses already exist
    if not Course.objects(title="Introduction to Python"):
        course_1 = Course(
        title="Introduction to Python",
        description="Learn Python programming from scratch.",
        category="Programming",
        instructors=["Instructor 1", "Instructor 2"],
        weeks={
            "week_1": WeeklyContent(
                videos=[
                    Video(video_id="vid_1", title="Intro to Python", url="http://example.com/video1", transcript="Transcript 1", duration=600),
                    Video(video_id="vid_2", title="Python Basics", url="http://example.com/video2", transcript="Transcript 2", duration=800),
                ],
                graded_assignments=[
                    Assignment(assignment_id="assign_1", questions=[
                        Question(question="What is Python?", options=["Language", "Animal"], correct_option=0),
                        Question(question="What does 'print()' do?", options=["Output", "Input"], correct_option=0),
                    ])
                ],
                practice_assignments=[
                    Assignment(assignment_id="practice_1", questions=[
                        Question(question="What is a variable in Python?", options=["Container", "Function"], correct_option=0),
                    ])
                ]  # Adding a sample practice assignment here
            )
        },
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )

        course_1.save()

    if not Course.objects(title="Data Structures"):
        course_2 = Course(
            title="Data Structures",
            description="Master the basics of data structures.",
            category="Computer Science",
            instructors=["Instructor 3"],
            weeks={
                "week_1": WeeklyContent(
                    videos=[
                        Video(video_id="vid_3", title="Intro to Arrays", url="http://example.com/video3", transcript="Transcript 3", duration=700),
                    ],
                    graded_assignments=[
                        Assignment(assignment_id="assign_2", questions=[
                            Question(question="What is an array?", options=["Collection", "Integer"], correct_option=0),
                        ])
                    ],
                    practice_assignments=[
                    Assignment(assignment_id="practice_1", questions=[
                        Question(question="What is a variable in Python?", options=["Container", "Function"], correct_option=0),
                    ])
                ]  # Adding a sample practice assignment here
                )
            },
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        course_2.save()

    # Check if students already exist
    if not Student.objects(email="alice@example.com"):
        student_1 = Student(
            name="Alice Johnson",
            email="alice@example.com",
            course_progress=[
                CourseProgress(
                    course_id=str(Course.objects(title="Introduction to Python").first().id),
                    weekly_progress={
                        "week_1": WeeklyProgress(
                            videos=[
                                VideoProgress(video_id="vid_1", status="completed"),
                                VideoProgress(video_id="vid_2", status="in_progress"),
                            ],
                            graded_assignments=[
                                AssignmentProgress(assignment_id="assign_1", score=8, max_score=10)
                            ],
                            practice_assignments=[AssignmentProgress(assignment_id="assign_1", score=8, max_score=10)]
                        )
                    }
                )
            ],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        student_1.save()

    if not Student.objects(email="bob@example.com"):
        student_2 = Student(
            name="Bob Smith",
            email="bob@example.com",
            course_progress=[
                CourseProgress(
                    course_id=str(Course.objects(title="Data Structures").first().id),
                    weekly_progress={
                        "week_1": WeeklyProgress(
                            videos=[
                                VideoProgress(video_id="vid_3", status="completed"),
                            ],
                            graded_assignments=[
                                AssignmentProgress(assignment_id="assign_2", score=10, max_score=10)
                            ],
                            practice_assignments=[AssignmentProgress(assignment_id="assign_1", score=8, max_score=10)]
                        )
                    }
                )
            ],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        student_2.save()

    print("Database seeding completed!")

