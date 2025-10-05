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
    model = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        system_instruction="You are Kelvin, a friendly, deeply empathetic, and supportive AI companion. Your goal is to listen, validate the user's feelings, and guide them gently. Do not give medical advice. Keep your responses concise and warm."
    )
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
    "https://kelvin-app-gamma.vercel.app",
    "https://kelvin-app-git-main-dhruvs-projects-0e302010.vercel.app",
    "https://kelvin-mkpog1abp-dhruvs-projects-0e302010.vercel.app",
    "http://localhost:3002",
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
    "Look out a window and notice 3 details you haven't before.",
    "Write down one small win from today.",
    "Close your eyes and count to 20 slowly.",
    "Compliment yourself in one sentence.",
    "Draw a doodle, no matter how simple.",
    "Do 10 jumping jacks.",
    "Smile for 15 seconds intentionally.",
    "Write down one goal for tomorrow.",
    "Take a slow sip of water and really taste it.",
    "Stand up and roll your shoulders 5 times.",
    "Look around and name 5 objects by color.",
    "Sit quietly and notice your breathing for 1 minute.",
    "Text someone 'thinking of you'.",
    "Write one kind thing about yourself.",
    "Clap your hands 10 times with energy.",
    "Take 3 minutes to stretch your legs.",
    "Look in the mirror and smile at yourself.",
    "Light a candle or turn on a soft light.",
    "Think of your favorite food and imagine the taste.",
    "Do one small chore you’ve been avoiding.",
    "Sit in silence for 2 minutes.",
    "Write a quick to-do list for tomorrow.",
    "Hum your favorite tune for 30 seconds.",
    "Find one object near you and really study it.",
    "Notice 5 sounds around you.",
    "Do a quick neck stretch side to side.",
    "Write down your current mood in 1 word.",
    "Imagine a place that makes you feel safe.",
    "Stand up and take 20 steps.",
    "Give yourself a mental high-five.",
    "Write down one thing you’re proud of.",
    "Unplug from screens for 2 minutes.",
    "List 3 things you like about your personality.",
    "Wash your face or hands slowly and mindfully.",
    "Look at something green around you.",
    "Take a slow deep breath and sigh out loudly.",
    "Imagine floating on water for 30 seconds.",
    "Organize one item on your desk.",
    "Stretch your fingers and hands for 20 seconds.",
    "Name 3 people you care about.",
    "Write one kind message to your future self.",
    "Stand near a window and feel the light.",
    "Notice the temperature of the air around you.",
    "Put on a song that makes you happy.",
    "Do 5 squats or simple movements.",
    "Smell something calming (tea, soap, spice).",
    "Write down your top 3 favorite hobbies.",
    "Pet an animal or imagine your favorite one.",
    "Practice saying 'I am enough'.",
    "Close your eyes and listen to your heartbeat.",
    "Think of one person who makes you smile.",
    "Do a gentle torso twist left and right.",
    "Notice your feet touching the ground.",
    "Turn off one unnecessary notification.",
    "Slowly count backwards from 30.",
    "Take one picture of something around you.",
    "Repeat a positive affirmation 3 times.",
    "Notice the sensation of your clothes on your skin.",
    "Stretch your legs forward and point your toes.",
    "Draw a tiny symbol that represents today.",
    "List 3 small things that went well today.",
    "Imagine your favorite smell vividly.",
    "Gently massage your temples for 10 seconds.",
    "Notice how your jaw feels and relax it.",
    "Name 3 colors you see right now.",
    "Say thank you to yourself for one thing.",
    "Take a mindful pause before your next action.",
    "Think about someone you admire.",
    "Turn your head slowly side to side.",
    "Stand tall and take a power pose for 20 seconds.",
    "Write one word that inspires you.",
    "Notice something beautiful around you.",
    "Give yourself permission to rest.",
    "Do one thing slower than usual on purpose.",
    "Write a note of encouragement for yourself.",
    "Say 'I am learning and growing'.",
    "Touch something with a new texture around you.",
    "Write down a place you’d love to visit.",
    "Take 5 seconds to appreciate silence.",
    "Blink slowly 5 times and rest your eyes.",
    "Imagine your happiest day vividly.",
    "Stretch your back gently while seated.",
    "Clean your phone screen.",
    "List 2 things you’re looking forward to.",
    "Whisper something kind to yourself.",
    "Smile and imagine sending it to someone else.",
    "Notice the rhythm of your breath.",
    "Stretch your neck upwards like a yawn.",
    "Write down a dream you’ve had.",
    "Tap your fingers rhythmically for 15 seconds.",
    "Imagine holding hands with someone you love.",
    "Tidy 3 items in your space.",
    "Sit up straight and breathe deeply.",
    "Write a silly sentence just for fun.",
    "Clap for yourself loudly once.",
    "Think of 3 foods you really enjoy.",
    "Spend 1 minute doing nothing on purpose.",
    "Notice the shadows around you.",
    "Stretch your arms overhead for 5 seconds.",
    "Name one kind act you can do tomorrow.",
    "Smell something familiar in your room.",
    "Take a photo of something ordinary.",
    "List 2 movies you like.",
    "Say 'I am safe right now'.",
    "Imagine the sound of waves or rain.",
    "Stretch your ankles in circles.",
    "Notice your breathing without changing it.",
    "Write down a random happy thought.",
    "Close your eyes and think of your favorite color.",
    "Look up at the ceiling and notice details.",
    "Pretend you are laughing for 10 seconds.",
    "Give a thumbs up to yourself.",
    "Write one hope for the next week.",
    "Stand near a window and take 3 breaths.",
    "Think of someone you can thank today.",
    "Imagine hugging your favorite person.",
    "List 3 songs you like.",
    "Look at something small and focus on details.",
    "Stretch your spine by reaching upwards.",
    "Take a slow, mindful sip of a drink.",
    "Say 'I am strong' three times.",
    "Tap your shoulders gently.",
    "Notice how the floor feels under you.",
    "Write one thing you love about mornings.",
    "Draw a quick smiley face.",
    "Say out loud: 'I matter'.",
    "Imagine a favorite childhood memory.",
    "Stretch your wrists gently.",
    "Take 30 seconds to breathe with your eyes closed.",
    "Look around for circles and count them.",
    "Give yourself a small hand massage.",
    "Smile and hold it for 5 breaths.",
    "Imagine your happiest future moment.",
    "Say thank you for something small.",
    "Stretch your chest open by pulling shoulders back.",
    "Notice the feeling of your hair or head.",
    "Draw a star quickly.",
    "Take 2 minutes to declutter.",
    "Whisper your favorite word.",
    "Think of 3 things you liked about today.",
    "Stand up and sway gently side to side.",
    "Notice one thing that feels soft.",
    "Write a message of kindness for someone.",
    "Look outside and describe the sky.",
    "Say 'I allow myself to rest'.",
    "Do 5 slow deep breaths with eyes closed.",
    "Stretch your side body gently.",
    "List 2 places you’d love to visit.",
    "Pat yourself gently on the back.",
    "Write one line of encouragement to yourself.",
    "Notice 3 textures in your environment.",
    "Say 'I am doing my best'.",
    "Draw a heart on paper.",
    "Close your eyes and picture your favorite flower.",
    "Listen closely to one quiet sound.",
    "Take one minute to sit still.",
    "Wiggle your toes slowly.",
    "Say 'I trust myself'.",
    "Write one lesson you learned today.",
    "Stretch your arms wide like wings.",
    "Notice 3 straight lines around you.",
    "Close your eyes and picture the ocean.",
    "Say 'I am grateful for this moment'.",
    "Write one good memory from this week.",
    "Place your hand on your chest and breathe deeply.",
    "Think of 2 things that relax you.",
    "Stretch your jaw by yawning.",
    "Look around for something round.",
    "Say something kind about your mind.",
    "List 3 things you like about evenings.",
    "Stand and shake out your arms.",
    "Write a word that makes you happy.",
    "Notice one sound inside your body.",
    "Smile and think 'I am okay'.",
    "Stretch your lower back gently.",
    "Say 'I forgive myself for today'.",
    "List 3 animals you like.",
    "Close your eyes and imagine stars.",
    "Take a deep belly breath.",
    "Stretch your legs forward for 10 seconds.",
    "Say 'I welcome peace'.",
    "Notice the warmth or coolness in the air.",
    "Think of 2 kind people you know.",
    "Write down your favorite season.",
    "Stand and balance on one foot for a few seconds.",
    "Smile and say 'I choose joy'.",
    "Take 10 seconds to notice your hands.",
    "Draw a wavy line freely.",
    "Think of your favorite book or story.",
    "Say 'I am calm'.",
    "Stretch your arms backward gently.",
    "Notice 3 square shapes around you.",
    "List 2 people who inspire you.",
    "Take a breath and count 5 heartbeats.",
    "Write one kind thing about someone else.",
    "Do a little shoulder dance.",
    "Notice the smell of the air.",
    "Say 'I am worthy'.",
    "Stretch your neck downward slowly.",
    "List 3 things you enjoyed recently.",
    "Write a silly word and laugh.",
    "Look for something shiny nearby.",
    "Say 'I let go of stress'.",
    "Pat your knees gently.",
    "Notice how your body feels seated.",
    "Imagine being in your favorite place.",
    "List 3 tiny wins you had today.",
    "Stretch both arms across your chest.",
    "Take 5 seconds to notice silence.",
    "Say 'I am present'.",
    "Draw something random.",
    "Think of one joke you know.",
    "Take 3 calming breaths slowly.",
    "Look around and find 2 patterns.",
    "Say 'I am loved'.",
    "Notice your heartbeat for a moment.",
    "Stretch your side body to each side.",
    "Write down one thing you’re curious about.",
    "Say 'I allow myself to relax'.",
    "Notice a color you rarely see.",
    "List 3 favorite childhood snacks.",
    "Smile and think of someone smiling back.",
    "Stretch your calves gently.",
    "Take a deep breath and sigh out.",
    "Write down a random word you like.",
    "Look at something small closely.",
    "Say 'I am okay where I am'.",
    "Notice how your shoulders feel.",
    "Stand and lift your arms upward.",
    "Think of 3 songs that make you dance.",
    "List 2 things you admire about yourself.",
    "Take a 1-minute screen break.",
    "Say 'I give myself permission to grow'.",
    "Notice one detail on your hand.",
    "Do 3 gentle squats.",
    "Write down your favorite fruit.",
    "Close your eyes and imagine rain sounds."
]

    chosen_quest = random.choice(quests)
    return QuestResponse(id=str(hash(chosen_quest)), text=chosen_quest)

@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
def post_chat(request: Request, chat_request: ChatRequest):
    user_message = chat_request.message.lower()
    crisis_keywords = ["kill myself", "want to die", "self harm"]
    if any(keyword in user_message for keyword in crisis_keywords):
        return ChatResponse(
            reply="It sounds like you are in crisis. Please reach out for help. You can connect with people who can support you by calling or texting 988 anytime in the US and Canada. In the UK, you can call 111."
        )

    if not model:
        return ChatResponse(reply="Sorry, the AI model is not configured correctly. Please check the server logs.")

    try:
        # Convert Pydantic history to a list of dicts for the Gemini library
        history = [h.dict() for h in chat_request.chat_history]

        response = chat_session.send_message(chat_request.message)

        return ChatResponse(reply=response.text)
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return ChatResponse(reply="Sorry, I had trouble connecting to the AI model.")