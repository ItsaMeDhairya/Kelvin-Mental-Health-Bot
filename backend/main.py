# 1. All imports
import os
import random
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.requests import Request
from slowapi.errors import RateLimitExceeded

# 2. Load environment variables
load_dotenv()

# 3. Configure Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"CRITICAL: Error configuring Gemini API: {e}")
    model = None

# 4. Create FastAPI app instance
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 5. Add CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://kelvin-app-gamma.vercel.app",
    "https://kelvin-app-git-main-dhruvs-projects-0e302010.vercel.app",
    "https://kelvin-mkpog1abp-dhruvs-projects-0e302010.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Define Pydantic Data Models
class ChatMessage(BaseModel):
    role: str
    parts: List[str]

class ChatRequest(BaseModel):
    message: str
    chat_history: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

class QuestResponse(BaseModel):
    id: str
    text: str

# 7. Define API Endpoints
system_instruction = """You are Kelvin, a supportive and empathetic companion. Your goal is to be a good listener and provide a safe space for users to reflect. Keep your responses concise (2-3 sentences). Do not give unsolicited advice. Your tone should be warm, encouraging, and gentle."""

@app.get("/")
def read_root():
    return {"message": "Kelvin Backend is running."}

@app.get("/api/quest/today", response_model=QuestResponse)
def get_daily_quest():
    quests = [
        "Take 5 deep, slow breaths.",
        "Write down one thing you are grateful for today.",
        "Step outside for 60 seconds of fresh air.",
        "Listen to one full song without any other distractions.",
        "Stretch your arms and back for 30 seconds.",
        "Drink a full glass of water.",
        "Tidy up one small area of your room.",
        "Send a positive message to a friend.",
        "Think of a happy memory for a moment.",
        "Look out a window and notice 3 details you haven't before."
    ]
    chosen_quest = random.choice(quests)
    return QuestResponse(id=str(hash(chosen_quest)), text=chosen_quest)

@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
def post_chat(request: Request, chat_request: ChatRequest):
    print(f"GEMINI_API_KEY loaded: {os.getenv('GEMINI_API_KEY') is not None}")
    user_message = chat_request.message.lower()
    crisis_keywords = ["kill myself", "want to die", "self harm"]
    if any(keyword in user_message for keyword in crisis_keywords):
        return ChatResponse(
            reply="It sounds like you are in crisis. Please reach out for help. You can connect with people who can support you by calling or texting 988 anytime in the US and Canada. In the UK, you can call 111."
        )

    if not model:
        return ChatResponse(reply="Sorry, the AI model is not configured correctly. Please check the server logs.")

    try:
        history = [h.dict() for h in chat_request.chat_history]
        print(f"Request body: {chat_request.dict()}")
        print(f"History being sent to Gemini: {history}")

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(f"{system_instruction} The user just said: {chat_request.message}")

        return ChatResponse(reply=response.text)
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return ChatResponse(reply="Sorry, I had trouble connecting to the AI model.")