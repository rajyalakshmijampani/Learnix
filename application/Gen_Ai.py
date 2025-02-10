import json
from pathlib import Path
import pickle
from langchain_google_genai import ChatGoogleGenerativeAI
from flask_restful import Resource
from flask import request, jsonify
import google.generativeai as genai
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import os

# Configure Google API key
with open('./secrets.json') as f:
    secrets = json.load(f)
GOOGLE_API_KEY = secrets["GOOGLE_API_KEY"]


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)


# Set API key (Store securely)
os.environ["GOOGLE_API_KEY"] = secrets["GOOGLE_API_KEY"]
#
class CourseAssistant(Resource):
    #example request
    ''' {
           "message": "How does deep learning differ?",
           "course_context": "AI and ML Course",
           "chat_history": [
             {"role": "user", "content": "What is machine learning?"},
             {"role": "assistant", "content": "Machine learning is a subset of AI..."}
           ]
         }'''
    def __init__(self):
        # Define prompt template (No system messages, as they are unsupported with API keys)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "Course Context: {course_context}\n\nUser: {message}")
            ]
        )

        # Initialize Gemini model with API key
        self.model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

    def post(self):
        try:
            data = request.get_json()
            if 'message' not in data:
                return jsonify({'error': 'Message is required'}), 400

            user_message = data['message']
            course_context = data.get('course_context', '')

            # Create the message chain
            chain = self.prompt | self.model
            response = chain.invoke({
                "course_context": course_context,
                "message": user_message
            })

            # Ensure the response is converted to a string
            ai_response = response.content if hasattr(response, "content") else str(response)

            return jsonify({
                'response': ai_response,
                'status': 'success'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        




faiss_folder = Path("FAISS")

# Load FAISS index for a given week
def load_faiss_for_week(week):
    faiss_index_path = faiss_folder / f"faiss_index_week{week}.pkl"
    if Path(faiss_index_path).exists():
        with open(faiss_index_path, "rb") as f:
            return pickle.load(f)
    else:
        print(f"No FAISS index found for Week {week}")
        return None

# Define Gemini LLM Wrapper
class GeminiLLM:
    def __init__(self, model_name):
        genai.configure(api_key=secrets["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel(model_name=model_name)

    def generate(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text if hasattr(response, "text") else str(response)

# Generate RAG prompt
def generate_rag_prompt(query, context, num_questions):
    return f"""
    You are Lumi, an AI assistant for the IIT Madras Business Analytics course. 
    You have access to course lectures, transcripts, and all related course materials. 
    Your role is to generate {num_questions} different and random multiple-choice questions (MCQs) based on the given context.

    The JSON should be a list of dictionaries, where each dictionary represents one MCQ.
    Each MCQ must have:
    - "question_statement": The question text.
    - "option_a": Option A
    - "option_b": Option B
    - "option_c": Option C
    - "option_d": Option D
    - "correct_option": The correct option (A, B, C, or D).

    QUERY: '{query}'
    CONTEXT: '{context}'
    Return a valid JSON response.
    """

# API Resource for generating questions
class GenerateQuestions(Resource):
    def post(self):
        try:
            data = request.get_json()
            week = data.get("week", 1)
            num_questions = data.get("num_questions", 3)
            user_query = data.get("query", f"Generate practice questions for week {week}")

            # Load FAISS for the requested week
            faiss_vector_store = load_faiss_for_week(week)
            if not faiss_vector_store:
                return jsonify({"error": f"No FAISS data available for week {week}"}), 400

            # Retrieve relevant context
            relevant_docs = faiss_vector_store.similarity_search(user_query, k=3)
            context = "\n".join([doc.page_content for doc in relevant_docs])

            # Initialize Gemini
            gemini_llm = GeminiLLM(model_name="gemini-1.5-flash")

            # Generate and invoke prompt
            prompt = generate_rag_prompt(user_query, context, num_questions)
            response = gemini_llm.generate(prompt)

            return jsonify({
                "status": "success",
                "week": week,
                "num_questions": num_questions,
                "mcqs": response
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Add these lines to __init__.py to register the new endpoints
# api.add_resource(CourseAssistant, '/chat/course')
# api.add_resource(CodeAssistant, '/chat/code')
