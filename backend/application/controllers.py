from application.models import User, Course, Lecture, Registration
from application import db, api
from flask import jsonify, request, jsonify, render_template, make_response
from flask_restful import Resource,fields, marshal
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
import secrets
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Any, List, Optional
from pydantic import Field
from langchain_huggingface import HuggingFaceEmbeddings
import pickle

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Import datastore here to avoid circular import
from application import create_datastore

# Initialize datastore where needed
datastore = create_datastore()

#---------------------------------- HOME API -------------------------------#

class Home(Resource):
    def get(self):
        html = render_template('index.html')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

#-------------------------------- USER PROFILE API -------------------------#
class User(Resource):
    # New User Registration
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({'error': 'Request body required', 'code': 400}),400)
            
            name = data.get('name')
            email = data.get('email')
            password = data.get("password")

            if not (name and email and password):
                return make_response(jsonify({'error': 'Name, Email and Password are required', 'code': 400}),400)
            
            user = datastore.find_user(email=email)
            if user:
                return make_response(jsonify({'error': 'Email already exists', 'code': 400}),400)

            user = datastore.create_user(name=name,email=email,password=generate_password_hash(password),roles=['user'])
            db.session.commit()

            # Register for default courses
            available_courses = Course.query.with_entities(Course.id).all()  # Fetch all course IDs
            registrations = [Registration(user_id=user.id, course_id=course.id) for course in available_courses]
            db.session.bulk_save_objects(registrations)  # Bulk insert for efficiency
            db.session.commit()

            return make_response(jsonify({'message': 'User registered successfully', 'code': 201}),201)

        except Exception as e:
            return make_response(jsonify({'error': str(e) , 'code': 500}),500)
    
    # Profile Update
    def put(self,mode):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({'error': 'Request body required', 'code': 400}), 400)
            
            if mode == 'profile':
                user_id = data.get("userId")
                new_name = data.get("name")
                new_email = data.get("email")

                if not user_id:
                    return make_response(jsonify({'error': 'User ID is required', 'code': 400}), 400)

                user = datastore.find_user(id=user_id)
                if not user:
                    return make_response(jsonify({"error": "User not found", 'code': 404}), 404)

                if new_name:
                    user.name = new_name
                if new_email:
                    existing_user = datastore.find_user(email=new_email)
                    if existing_user and existing_user.id != user_id:
                        return make_response(jsonify({'error': 'Email already exists', 'code': 400}), 400)
                    user.email = new_email

                db.session.commit()

                return make_response(jsonify({"message": "User profile updated successfully", 'code': 200}), 200)

            elif mode == 'password':
                user_id = data.get('userId')
                old_password = data.get('oldPassword')
                new_password = data.get('newPassword')

                if not (user_id and old_password and new_password):
                    return make_response(jsonify({"error": "All fields are required",'code':400}), 400)
                
                user = datastore.find_user(id=user_id)
                if not user:
                    return make_response(jsonify({"error": "User not found",'code':404}), 404)
                if not check_password_hash(user.password, old_password):
                    return make_response(jsonify({"error": "Incorrect old password",'code':400}), 400)
                
                user.password = generate_password_hash(new_password)

                db.session.commit()

                return make_response(jsonify({"message": "Password changed successfully",'code': 200}), 200)

        except Exception as e:
            return make_response(jsonify({'error': str(e), 'code': 500}), 500)

#---------------------------------------------USER LOGIN API ------------------------#
user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "name": fields.String
    }

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({'error': 'Request body required', 'code': 400}),400)
            
            email = data.get('email')
            password = data.get("password")

            if not (email and password):
                return make_response(jsonify({'error': 'Email and Password are required', 'code': 400}),400)

            user = datastore.find_user(email=email)
            if not user or not check_password_hash(user.password,password):
                return make_response(jsonify({'error': 'Invalid Credentials', 'code': 400}), 400)

            marshalled_data = marshal(user, user_fields)
            return make_response(jsonify(**marshalled_data,**{'token':secrets.token_urlsafe(32),'code':200}),200)

        except Exception as e:
            return make_response(jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)}),500)

#---------------------------------- USER DASHBOARD API -------------------------------#

class UserDashboard(Resource):
    def get(self):
        html = render_template('dashboard.html')
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        return response

#--------------------------------------------REGISTERED COURSES API---------------------#
class UserCurrentCourses(Resource):
    def get(self, user_id):
        try:
            registered_subquery = select(Registration.course_id).where(Registration.user_id == user_id)
            
            registered_courses = Course.query.with_entities(Course.id, Course.name).filter(Course.id.in_(registered_subquery)).all()
           
            result = [{"id": course[0], "name": course[1]} for course in registered_courses]

            return make_response(jsonify(result), 200)
        
        except Exception as e:
            return make_response(jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)}),500)
        
#------------------------------------------LECTURES API---------------------------------#
class GetAllLectures(Resource):
    def get(self, id):
        try:
            lectures = Lecture.query.filter_by(course_id=id).all()
            
            lectures_data = []
            for lecture in lectures:
                lectures_data.append({
                    'lecturenumber': lecture.lectureNumber,
                    'title': lecture.title,
                    'link': lecture.link,
                    'weeknumber': lecture.weekNumber,
                })
            
            return make_response(jsonify(lectures_data), 200)
        
        except Exception as e:
            return make_response(jsonify({'error': 'Something went wrong', 'code': 500, 'message': str(e)}),500)

#----------------------------------------------MOCK QUESTIONS API-----------------------------#

# Function to load FAISS index based on user input week
def load_faiss_for_week(week):
    faiss_folder = os.path.join(base_dir, '..','FAISS')
    faiss_index_path = os.path.join(faiss_folder, f"faiss_index_week{week}.pkl")
    try:
        with open(faiss_index_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading FAISS index for Week {week} : {str(e)}")
        return None

response_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question_statement": {"type": "string"},
            "option_a": {"type": "string"},
            "option_b": {"type": "string"},
            "option_c": {"type": "string"},
            "option_d": {"type": "string"},
            "correct_answer": {"type": "string"},
        },
        "required": ["question_statement","option_a","option_b","option_c","option_d","correct_answer"],
    },
}

class MockQuestions(Resource):
    def __init__(self):
        self.gemini_llm = self._initialize_gemini_llm()
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
    def _initialize_gemini_llm(self):
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        return model
    
    def _generate_rag_prompt(self, query, context,num_questions):
        return f"""
        You are Lumi, an AI assistant for the IIT Madras Business Analytics course. You have access to course lectures, transcripts, and all related course materials.
        Your role is to generate {num_questions} different and random multiple-choice questions (MCQ) based on the given context. 
        Please generate the MCQs in JSON format.
        The JSON should be a list where each element is a dictionary representing one MCQ. 
        Each MCQ dictionary must have the following keys:
        - "question_statement": The question text.
        - "option_a": Option A
        - "option_b": Option B
        - "option_c": Option C
        - "option_d": Option D
        - "correct_option": The correct option (A, B, C, or D).

        QUERY: '{query}'
        CONTEXT: '{context}'
        """
    
    def _retrieve_context(self, user_input,week):
        # Retrieve relevant context from FAISS store
        faiss_vector_store = load_faiss_for_week(week)
        if not faiss_vector_store:
            return "No data available for this week."
        
        relevant_docs = faiss_vector_store.similarity_search(user_input, k=3)
        return "\n".join([doc.page_content for doc in relevant_docs])

    def _warm_up_model(self):
        # Optional warm-up for the model
        warm_up_prompt = self._generate_rag_prompt(query="Hello, how are you?")
        _ = self.gemini_llm.generate_content(warm_up_prompt)
        
    def generate(self, user_input,week, num_questions):
        # Main method to generate questions
        context = self._retrieve_context(user_input, week)
        if context == "No data available for this week.":
            return context
        
        prompt = self._generate_rag_prompt(query=user_input, context=context, num_questions=num_questions)
        return self.gemini_llm.generate_content(prompt,
                                                generation_config={"response_mime_type": "application/json",
                                                                  "response_schema": response_schema,
                                                }).text

    def get(self):

        # Flask API route to handle GET requests
        try:
            week = request.args.get('week', default=1, type=int)
            num_questions = request.args.get('num_questions', default=3, type=int)

            user_query = f"Generate practice questions for week {week}"
            response = self.generate(user_query,week, num_questions)
            
            return make_response(jsonify({"mcqs": response, "code": 200}), 200)
        
        except Exception as e:
            return make_response(jsonify({"error": str(e), "code": 500}), 500)
        
#----------------------------------------------CHAT SUPPORT API-----------------------------#

class ChatSupport(Resource):
    def __init__(self):
        # Configure Gemini model
        genai.configure(api_key=gemini_api_key)
        self.gemini_llm = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    def post(self):
        try:
            # Get request data
            data = request.get_json()
            message = data.get("message")
            chat_history = data.get("chat_history", [])

            if not message:
                return make_response(jsonify({"error": "Message is required", "code": 400}), 400)

            # Prepare the chat history for the model
            history = "\n".join([f"{item['role']}: {item['content']}" for item in chat_history])
            prompt = f"""
            You are an intelligent and helpful assistant. Continue the conversation based on the following chat history.
            Your answers should be concise and to the point, no more than five sentences unless needed.
            {history}
            User: {message}
            Assistant:
            """

            # Get response from Gemini model
            response = self.gemini_llm.generate_content(prompt)
            reply = response.text.strip()

            return make_response(jsonify({"response": reply, "code": 200}), 200)
        
        except Exception as e:
            return make_response(jsonify({"error": str(e), "code": 500}), 500)


#-----------------------------------------------LOGOUT API----------------#
class Logout(Resource):
    def post(self):
        try:
            response = make_response(jsonify({"message": "Successfully logged out", "code": 200}),200)
            return response
        
        except Exception as e:
            return make_response(jsonify({"error": str(e), "code": 500}),500)
        
api.add_resource(Home, "/")
api.add_resource(User, "/user","/user/<string:mode>")
api.add_resource(Login, "/login")
api.add_resource(UserCurrentCourses, "/user/<int:user_id>/currentcourses")
api.add_resource(GetAllLectures,"/get_all_lectures/<int:id>")
api.add_resource(MockQuestions,'/mock')
api.add_resource(ChatSupport,"/chat")
api.add_resource(Logout, "/logout")