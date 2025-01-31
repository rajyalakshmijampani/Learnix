
from mongoengine import connect
from application.models import Student, Course

def clear_mongodb():
    # Connect to MongoDB
    connect('my_database', host='localhost', port=27017)
    
    # Drop collections
    Student.drop_collection()
    Course.drop_collection()
    
    print("MongoDB collections cleared successfully!")

if __name__ == "__main__":
    clear_mongodb()