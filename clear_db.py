from mongoengine import connect
from application.models import Student, Course
from application.database import db
from flask import Flask
from application.config import Config

def clear_all_databases():
    # Clear MongoDB
    connect('my_database', host='localhost', port=27017)
    Student.drop_collection()
    Course.drop_collection()
    print("MongoDB collections cleared!")

    # Clear SQLite
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("SQLite database cleared!")

if __name__ == "__main__":
    clear_all_databases()
