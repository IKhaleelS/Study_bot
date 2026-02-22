from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from database import chat_collection, get_chat_history, clear_chat_history
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Study Bot API", description="AI-powered Study Assistant")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq model with correct endpoint
try:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",  # Using OpenAI GPT model via Groq
        temperature=0.3
    )
except Exception as e:
    print(f"Error initializing Groq model: {e}")
    raise

# Cybersecurity-focused system prompt
system_prompt = """
You are a helpful study assistant specialized in computer science, engineering, cybersecurity and technology.
You provide detailed explanations and step-by-step solutions to questions related to these fields.
Be friendly and engaging in your responses.

Focus on contextual teaching and provide well-structured answers.
When appropriate, use examples and break down complex topics into digestible parts.
"""

# Pydantic model for request validation
class QuestionRequest(BaseModel):
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {"question": "What is a SQL injection attack?"}
        }


@app.get("/", tags=["Health"])
def home():
    """Health check endpoint"""
    return {
        "message": "Study Bot is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/ask", tags=["Chat"])
def ask(request: QuestionRequest):
    """
    Ask the study bot a question and get an AI response.
    The conversation is stored in MongoDB for history tracking.
    """
    question = request.question.strip()
    
    # Input validation
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if len(question) > 5000:
        raise HTTPException(status_code=400, detail="Question too long (max 5000 characters)")
    
    try:
        # Build messages with context
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
        
        # Get AI response
        response = llm.invoke(messages)
        
        # Save the conversation to MongoDB with timestamp
        chat_record = {
            "question": question,
            "response": response.content,
            "timestamp": datetime.now(),
            "model": "openai/gpt-oss-120b"
        }
        chat_collection.insert_one(chat_record)
        
        return {
            "response": response.content,
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing your question: {str(e)}")


@app.get("/history", tags=["Chat"])
def history(limit: int = 10):
    """
    Retrieve chat history from MongoDB.
    
    Args:
        limit: Number of recent messages to retrieve (default: 10)
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        chats = get_chat_history(limit)
        return {
            "success": True,
            "count": len(chats),
            "history": chats
        }
    except Exception as e:
        print(f"Error retrieving history: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving chat history")


@app.delete("/clear-history", tags=["Chat"])
def clear_history():
    """
    Clear all chat history from the database.
    Warning: This action cannot be undone.
    """
    try:
        result = clear_chat_history()
        return {
            "success": True,
            "message": f"Cleared {result} chat records",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail="Error clearing chat history")


@app.get("/stats", tags=["Analytics"])
def stats():
    """Get basic statistics about the chatbot usage"""
    try:
        total_chats = chat_collection.count_documents({})
        return {
            "success": True,
            "total_conversations": total_chats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")