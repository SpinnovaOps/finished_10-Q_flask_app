from app.utils.mongo_utils import users_collection

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # In production, hash this!

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        users_collection.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        return users_collection.find_one({"username": username})