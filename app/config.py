from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY", "7a1f7c7b43e8be2f7418b3211121c25cab084be0a5aa88b67c35e37f5395bf3e")