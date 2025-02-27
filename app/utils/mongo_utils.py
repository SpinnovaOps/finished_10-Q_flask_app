from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client["pdf_data"]

users_collection = db["users"]
documents_collection = db["documents"]
sections_collection = db["sections"]