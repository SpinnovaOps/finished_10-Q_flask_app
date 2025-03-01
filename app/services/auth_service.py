from app.models.user_model import User
from flask import session

class AuthService:
    @staticmethod
    def signup(username, email, password):
        if User.find_by_username(username):
            raise ValueError("Username already exists")
        user = User(username, email, password)
        user.save()
        return {"message": "success!! Registered"}

    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and user["password"] == password:  # In production, hash passwords
            session["username"] = username
            return {"message": "login successful"}
        raise ValueError("Invalid credentials")

    @staticmethod
    def logout():
        session.pop("username", None)
        return {"message": "user is logged out"}