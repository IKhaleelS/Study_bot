# Render Deployment Guide

## Deployment Steps for Render

### 1. Create Render Account
- Go to https://render.com
- Sign up and connect your GitHub repository

### 2. Deploy on Render

**Web Service Setup:**
1. Click "New +" → "Web Service"
2. Connect your Study_bot GitHub repository
3. Configure:
   - **Name**: study-bot (or your preference)
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (for testing) or Starter (for production)

### 3. Set Environment Variables
In Render Dashboard → Environment:

```
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URL=your_mongodb_connection_string
DEBUG=False
```

### 4. Deploy MongoDB
- Use MongoDB Atlas (free tier available at https://mongodb.com/atlas)
- Create a cluster
- Get connection string and add to Render environment

### 5. Monitor Deployment
- Logs appear in real-time
- Check for errors: "✓ MongoDB connected successfully!"
- Your app will be live at: `https://study-bot.onrender.com`

## Production Considerations

### CORS Configuration
Update `main.py` before deploying:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your frontend domain
    allow_credentials=True,
)
```

### Environment-Specific Settings
```python
# For production:
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
if not DEBUG:
    # Add production-specific security headers
```

### Performance
- First request may be slow (cold start)
- Free tier sleeps after 15 minutes of inactivity
- Upgrade to Starter plan for persistent uptime

## Troubleshooting

**MongoDB Connection Fails on Render:**
- Check IP whitelist in MongoDB Atlas
- Add `0.0.0.0/0` or Render's IP range

**Import Errors:**
- Ensure all dependencies in requirements.txt
- Run `pip freeze > requirements.txt` locally to update

**CORS Errors from Frontend:**
- Add frontend URL to allow_origins list
- For testing, use `["*"]`

## Monitoring
- View logs: Render Dashboard → Logs tab
- Set up error tracking: https://sentry.io (free tier)

---

See README.md for API documentation after deployment.
