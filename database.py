import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable not set")

client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("✓ MongoDB connected successfully!")
except ServerSelectionTimeoutError:
    print("✗ MongoDB connection timeout - check your MONGODB_URL")
    raise
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    raise

db = client["studybot_db"]
chat_collection = db["chat_history"]

# Create index for better query performance
try:
    chat_collection.create_index("timestamp")
    print("✓ Database indexes created")
except Exception as e:
    print(f"Note: Index creation: {e}")


def get_chat_history(limit: int = 10):
    """
    Retrieve recent chat history from MongoDB.
    
    Args:
        limit: Number of recent chats to retrieve
        
    Returns:
        List of chat records sorted by most recent
    """
    try:
        chats = list(
            chat_collection.find()
            .sort("timestamp", -1)
            .limit(limit)
        )
        # Convert ObjectId to string for JSON serialization
        for chat in chats:
            chat["_id"] = str(chat["_id"])
            chat["timestamp"] = chat["timestamp"].isoformat() if isinstance(chat["timestamp"], datetime) else chat["timestamp"]
        return chats
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []


def clear_chat_history():
    """
    Clear all chat history from the database.
    
    Returns:
        Number of deleted records
    """
    try:
        result = chat_collection.delete_many({})
        return result.deleted_count
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        raise