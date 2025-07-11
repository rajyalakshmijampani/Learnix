import pytest
from flask import Flask , jsonify , request
from flask.testing import FlaskClient
from application import app,db
from application.models import *



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # with app.app_context():
        #     db.drop_all()


#Registration API
def test_register_new_user(client:FlaskClient):
    data={
        "email":"test123@gmail.com",
        "password":"password",
        "name":"test"
    }
    response=client.post('/user',json=data)
    assert response.status_code==201
    assert response.json=={'message': 'User registered successfully', 'code': 201}

    """
    Test Case: Register a new user
    API endpoint: /user
    Method: POST
    Expected Output: {'message': 'User registered successfully', 'code': 201}
    Actual Output: {'message': 'User registered successfully', 'code': 201}
    Result: PASS
    """

def test_register_existing_user(client:FlaskClient):
    data={
        "email":"test123@gmail.com",
        "password":"password",
        "name":"test"
    }
    response=client.post('/user',json=data)
    print(response.json)
    assert response.status_code==400
    assert response.json=={'error': 'Email already exists', 'code': 400}
    """
    Test Case: Register an existing user
    API endpoint: /user
    Method: POST
    Expected Output: {'error': 'Email already exists', 'code': 400}
    Actual Output: {'error': 'Email already exists', 'code': 400}
    Result: PASS
    """

def test_register_missing_field(client:FlaskClient):
    data={
        "email":"test456@gmail.com"
    }
    response=client.post('/user',json=data)
    assert response.status_code==400
    assert response.json=={'error': 'Name, Email and Password are required', 'code': 400}
    """
    Test Case: Register a user with missing fields
    API endpoint: /user
    Method: POST
    Expected Output: {'error': 'Name, Email and Password are required', 'code': 400}
    Actual Output: {'error': 'Name, Email and Password are required', 'code': 400}
    Result: PASS
    """

#Login API
def test_login_success(client:FlaskClient):
    login_data = {
        "email": "test123@gmail.com",
        "password": "password"
    }
    response = client.post('/login', json=login_data)
    print(response.json)
    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["email"] == "test123@gmail.com"
    assert response.json["name"] == "test"
    """
    Test Case: Successful login with valid credentials
    API endpoint: /login
    Method: POST
    Expected Output: {
        "email": "test123@gmail.com",
        "name": "test",
        "token": "<random_token>",
        "code": 200
    }
    Actual Output: {
        "email": "test123@gmail.com",
        "name": "test",
        "token": "<random_token>",
        "code": 200
    }
    Result: PASS
    """

def test_login_invalid_credentials(client:FlaskClient):
    data = {
        "email": "wrong@gmail.com",
        "password": "wrongpassword"
    }
    response = client.post('/login', json=data)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid Credentials', 'code': 400}
    """
    Test Case: Login with invalid credentials
    API endpoint: /login
    Method: POST
    Expected Output: {'error': 'Invalid Credentials', 'code': 400}
    Actual Output: {'error': 'Invalid Credentials', 'code': 400}
    Result: PASS
    """

def test_login_without_data(client:FlaskClient):
    response = client.post('/login', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Request body required', 'code': 400}
    """
    Test Case: Login attempt without request body
    API endpoint: /login
    Method: POST
    Expected Output: {'error': 'Request body required', 'code': 400}
    Actual Output: {'error': 'Request body required', 'code': 400}
    Result: PASS
    """

def test_login_missing_credentials(client:FlaskClient):
    response = client.post('/login', json={"email": "test@gmail.com"})
    assert response.status_code == 400
    assert response.json == {'error': 'Email and Password are required', 'code': 400}
    """
    Test Case: Login attempt with missing password
    API endpoint: /login
    Method: POST
    Expected Output: {'error': 'Email and Password are required', 'code': 400}
    Actual Output: {'error': 'Email and Password are required', 'code': 400}
    Result: PASS
    """

#Profile Update API
def test_update_profile_success(client:FlaskClient):    
    update_data = {
        "userId": 1,
        "name": "updated name",
        "email": "updated@gmail.com"
    }
    response = client.put('/user/profile', json=update_data)
    print(response.json)
    assert response.status_code == 200
    assert response.json == {"message": "User profile updated successfully", 'code': 200}
    """
    Test Case: Successfully update user profile
    API endpoint: /user/profile
    Method: PUT
    Expected Output: {"message": "User profile updated successfully", 'code': 200}
    Actual Output: {"message": "User profile updated successfully", 'code': 200}
    Result: PASS
    """

def test_update_profile_no_user(client:FlaskClient):
    update_data = {
        "userId": 999,
        "name": "updated name"
    }
    response = client.put('/user/profile', json=update_data)
    assert response.status_code == 404
    assert response.json == {"error": "User not found", 'code': 404}
    """
    Test Case: Update profile for non-existent user
    API endpoint: /user/profile
    Method: PUT
    Expected Output: {"error": "User not found", 'code': 404}
    Actual Output: {"error": "User not found", 'code': 404}
    Result: PASS
    """

def test_change_password_success(client:FlaskClient):
    password_data = {
        "userId": 1,
        "oldPassword": "password",
        "newPassword": "password2"
    }
    response = client.put('/user/password', json=password_data)
    print(response.json)
    assert response.status_code == 200
    assert response.json == {"message": "Password changed successfully", 'code': 200}
    """
    Test Case: Successfully change user password
    API endpoint: /user/password
    Method: PUT
    Expected Output: {"message": "Password changed successfully", 'code': 200}
    Actual Output: {"message": "Password changed successfully", 'code': 200}
    Result: PASS
    """

def test_change_password_wrong_old_password(client:FlaskClient):
    
    password_data = {
        "userId": 1,
        "oldPassword": "wrongpassword",
        "newPassword": "newpassword"
    }

    response = client.put('/user/password', json=password_data)
    print(response.json)
    assert response.status_code == 400
    assert response.json == {"error": "Incorrect old password", 'code': 400}
    """
    Test Case: Change password with incorrect old password
    API endpoint: /user/password
    Method: PUT
    Expected Output: {"error": "Incorrect old password", 'code': 400}
    Actual Output: {"error": "Incorrect old password", 'code': 400}
    Result: PASS
    """

#Current Courses API
def test_get_user_courses(client:FlaskClient):
    
    response = client.get('/user/1/currentcourses')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Each course should have id and name
    if len(response.json) > 0:
        assert all('id' in course and 'name' in course for course in response.json)
    """
    Test Case: Get user's current courses
    API endpoint: /user/<user_id>/currentcourses
    Method: GET
    Expected Output: [
        {"id": 1, "name": "Course 1"},
        {"id": 2, "name": "Course 2"}
    ]
    Actual Output: List of courses with id and name fields
    Result: PASS
    """

#Lectures API
def test_get_course_lectures(client:FlaskClient):
    response = client.get('/get_all_lectures/1')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Each lecture should have required fields
    if len(response.json) > 0:
        assert all(
            'lecturenumber' in lecture 
            and 'title' in lecture 
            and 'link' in lecture 
            and 'weeknumber' in lecture 
            for lecture in response.json
        )
    """
    Test Case: Get course lectures
    API endpoint: /get_all_lectures/<course_id>
    Method: GET
    Expected Output: [
        {
            "lecturenumber": 1,
            "title": "Lecture 1",
            "link": "lecture_link",
            "weeknumber": 1
        }
    ]
    Actual Output: List of lectures with required fields
    Result: PASS
    """

#Mock Questions API
def test_get_mock_questions(client:FlaskClient):
    response = client.get('/mock?week=1&num_questions=3')
    assert response.status_code == 200
    assert "mcqs" in response.json
    """
    Test Case: Get mock questions
    API endpoint: /mock
    Method: GET
    Expected Output: List of MCQs
    Result: PASS
    """

#Chat Support API
def test_chat_support(client:FlaskClient):
    data = {
        "message": "What is Business Analytics?",
        "chat_history": []
    }
    response = client.post('/chat', json=data)
    assert response.status_code == 200
    assert "response" in response.json
    """
    Test Case: Chat support interaction
    API endpoint: /chat
    Method: POST
    Expected Output: AI response
    Result: PASS
    """

#Logout API
def test_logout(client:FlaskClient):
    response = client.post('/logout')
    assert response.status_code == 200
    assert response.json == {"message": "Successfully logged out", "code": 200}
    """
    Test Case: User logout
    API endpoint: /logout
    Method: POST
    Expected Output: {"message": "Successfully logged out", "code": 200}
    Actual Output: {"message": "Successfully logged out", "code": 200}
    Result: PASS
    """

def test_chat_support_empty_message(client:FlaskClient):
    data = {
        "message": "",
        "chat_history": []
    }
    response = client.post('/chat', json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Message is required", "code": 400}
    """
    Test Case: Chat support with empty message
    API endpoint: /chat
    Method: POST
    Expected Output: {"error": "Message is required", "code": 400}
    Result: PASS
    """

def test_invalid_week_mock_questions(client:FlaskClient):
    response = client.get('/mock?week=999&num_questions=3')
    assert response.status_code == 200
    assert "No data available for this week." in str(response.json)
    """
    Test Case: Get mock questions for invalid week
    API endpoint: /mock
    Method: GET
    Expected Output: Error message about no data
    Result: PASS
    """

