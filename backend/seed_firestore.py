import os
from google.cloud import firestore

# Ensure the script uses the correct project
# In a real GCP environment, you might not need to set this explicitly
# if the environment is already configured.
# os.environ["GCLOUD_PROJECT"] = "your-gcp-project-id"

# Initialize Firestore DB Client
db = firestore.Client()

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

# Add each quest to the 'quests' collection
for quest_text in quests:
    db.collection('quests').add({'text': quest_text})

print(f"Successfully seeded {len(quests)} quests to Firestore.")
