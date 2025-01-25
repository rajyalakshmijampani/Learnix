# application/auth_apis.py
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from application.database import db
from .models import *



class UserRegistration(Resource):
    def post(self):
        try:
            data = request.json
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role_name = data.get('role', 'customer')  # Default to 'customer' role

            if User.query.filter_by(username=username).first():
                return {"msg": "Username already exists"}, 400
            if User.query.filter_by(email=email).first():
                return {"msg": "Email already exists"}, 400

            hashed_password = generate_password_hash(password)
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                return {"msg": f"Role '{role_name}' does not exist"}, 400

            new_user = User(username=username, email=email, password=hashed_password)
            new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()

            return {"msg": "User created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": "Error creating user", "error": str(e)}, 500

class UserLogin(Resource):
    def post(self):
        try:
            data = request.json
            # username = data.get('username')
            password = data.get('password')
            email=data.get('email')
            if not email or not password:
                return {"msg": "Missing username or password"}, 400

            user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return {"msg": "Invalid credentials"}, 401

            access_token = create_access_token(identity=user.id)

            return jsonify({
                "msg": "Login successful",
                "access_token": access_token
            })
        except Exception as e:
            return {"msg": "Error logging in", "error": str(e)}, 500

class ProtectedResource(Resource):
    @role_required('admin')  # Protecting this resource for 'admin' only
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return {"msg": "User not found"}, 404

        return jsonify({
            "msg": "This is a protected resource",
            "user": {
                "username": user.username,
                "email": user.email
            }
        })

class AssignRole(Resource):
    @role_required('admin')  # Only admin can assign roles
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return {"msg": "User not found"}, 404

            data = request.json
            role_name = data.get('role')

            role = Role.query.filter_by(name=role_name).first()
            if not role:
                return {"msg": f"Role '{role_name}' does not exist"}, 400

            if role not in current_user.roles:
                current_user.roles.append(role)
                db.session.commit()

            return {"msg": f"Role '{role_name}' assigned successfully to user"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": "Error assigning role", "error": str(e)}, 500

class RoleList(Resource):
    @role_required('admin')  # Only admin can list roles
    def get(self):
        try:
            roles = Role.query.all()
            roles_list = [{"id": role.id, "name": role.name, "description": role.description} for role in roles]
            return jsonify({"roles": roles_list})
        except Exception as e:
            return {"msg": "Error retrieving roles", "error": str(e)}, 500
