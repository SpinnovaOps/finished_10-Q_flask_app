from flask import request, jsonify, session
from app.services.auth_service import AuthService

def signup():
    data = request.get_json()
    if not data or not all(key in data for key in ["username", "emailid", "password"]):
        return jsonify({"error": "Missing required fields: username, emailid, password"}), 400

    username = data["username"]
    emailid = data["emailid"]
    password = data["password"]

    # Input validation
    if not isinstance(username, str) or not isinstance(emailid, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid input types"}), 400
    if len(username) < 3 or len(password) < 6:
        return jsonify({"error": "Username must be at least 3 chars, password at least 6 chars"}), 400

    try:
        result = AuthService.signup(username, emailid, password)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def login():
    data = request.get_json()
    if not data or not all(key in data for key in ["username", "password"]):
        return jsonify({"error": "Missing required fields: username, password"}), 400

    username = data["username"]
    password = data["password"]

    # Input validation
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid input types"}), 400

    try:
        user = AuthService.login(username, password)
        session["username"] = username  # Store username in session
        return jsonify({"message": "login successful"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

def logout():
    session.pop("username", None)  # Clear session
    return jsonify({"message": "user is logged out"}), 200