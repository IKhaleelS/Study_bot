# Study Bot

An AI-powered study assistant API built with FastAPI and LangChain, providing intelligent answers to questions about computer science, engineering, cybersecurity, and technology.

## Features

- AI-powered responses using Groq LLM
- MongoDB integration for conversation history
- RESTful API with automatic documentation
- CORS enabled for frontend integration
- Input validation and error handling
- Chat history management

## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (free tier available)
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/IKhaleelS/Study_bot.git
cd Study_bot
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env   # macOS/Linux

# Edit .env with your credentials:
GROQ_API_KEY=your_groq_api_key
MONGODB_URL=your_mongodb_connection_string
DEBUG_MODE=True
```

## Setup Instructions

### Get Groq API Key
1. Visit https://console.groq.com
2. Sign up and create an API key
3. Add to .env file

### MongoDB Setup
1. Create account at https://mongodb.com/atlas
2. Create a free cluster
3. Get connection string
4. Add to .env file

## Running Locally

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /ask | Send question and get response |
| GET | /history | Get chat history |
| GET | /stats | Get usage statistics |
| DELETE | /clear-history | Clear all chat records |

### Example Usage

Ask a question:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is cybersecurity?"}'
```

Get chat history:
```bash
curl "http://localhost:8000/history?limit=10"
```

## Deployment

### Render

1. Push code to GitHub
2. Go to render.com and create new Web Service
3. Connect your GitHub repository
4. Set environment variables:
   - GROQ_API_KEY
   - MONGODB_URL
   - DEBUG=False
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Deploy

See RENDER_DEPLOYMENT.md for detailed instructions.

## Project Structure

```
Study_bot/
├── main.py              # FastAPI application
├── database.py          # MongoDB integration
├── index.html           # Web interface
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (local only)
├── .env.example         # Environment template
└── .gitignore           # Git ignore rules
```

## Technologies

- FastAPI: Web framework
- LangChain: LLM integration
- Groq: LLM provider
- MongoDB: Database
- Python 3.8+: Runtime

## Security

- All credentials stored in .env (not committed)
- .env file is gitignored
- API has input validation
- CORS configured
- Error handling on all endpoints

## Troubleshooting

**MongoDB Connection Error:**
```
Check MONGODB_URL in .env
Verify IP whitelist in MongoDB Atlas
Ensure internet connection is stable
```

**Groq API Error:**
```
Verify GROQ_API_KEY is correct at console.groq.com
Check API rate limits
Ensure valid API key format
```

**Module Not Found:**
```
Run: pip install -r requirements.txt
Verify virtual environment is activated
Check Python version is 3.8+
```

## Error Handling

All API endpoints return structured error responses:
- 400: Invalid request (empty question, too long, invalid format)
- 500: Server error (database, API, or processing error)

## Future Improvements

- Conversation memory with context awareness
- User authentication and personalized history
- Response streaming for real-time updates
- Rate limiting per user
- Multi-language support
- Subject-specific filtering

## License

MIT License

## Support

For issues and questions, please create an issue in the GitHub repository.
