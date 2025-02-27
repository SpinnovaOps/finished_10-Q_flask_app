from pymongo import MongoClient
from dotenv import load_dotenv
import os
import ssl
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

def test_mongodb_connection():
    client = None
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not set in .env file.")

        if not (mongo_uri.startswith("mongodb://") or mongo_uri.startswith("mongodb+srv://")):
            raise ValueError(f"Invalid URI scheme: URI must begin with 'mongodb://' or 'mongodb+srv://'. Current URI: {mongo_uri}")

        # Print SSL version for debugging
        print(f"SSL Version: {ssl.OPENSSL_VERSION}")

        # Create MongoClient with TLS enabled (default for Atlas)
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=60000,  # 60 seconds
            connectTimeoutMS=20000,  # 20 seconds
            socketTimeoutMS=20000,  # 20 seconds
            tls=True,  # Explicitly enable TLS (replaces ssl=True)
            tlsCAFile=None,  # Use system CA certificates (default for Atlas)
            tlsCertificateKeyFile=None  # Not needed for Atlas
        )

        client.admin.command("ping")
        db = client["pdf_data"]
        collections = db.list_collection_names()
        print("Successfully connected to MongoDB Atlas!")
        print(f"Available collections: {collections}")

        test_collection = db["test_collection"]
        test_collection.insert_one({"test": "connection_successful", "timestamp": "2025-02-26"})
        print("Test document inserted successfully.")
        test_collection.delete_many({"test": "connection_successful"})
        print("Test document removed.")

    except Exception as e:
        logger.error(f"Failed to connect to MongoDB Atlas. Error: {str(e)}")
        return False

    finally:
        if client is not None:
            client.close()
            print("MongoDB connection closed.")

    return True

if __name__ == "__main__":
    if test_mongodb_connection():
        print("Connection test passed!")
    else:
        print("Connection test failed. Please check your connection string, credentials, and network settings.")