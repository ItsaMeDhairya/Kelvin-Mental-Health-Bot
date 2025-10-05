# Project Overview

This is a web application called "Kelvin," designed to be a supportive and empathetic AI companion. The project is a full-stack application with a Next.js frontend and a Python FastAPI backend.

## Frontend

The frontend is a Next.js application located in the `frontend` directory. It uses React, and Tailwind CSS for styling. The main pages are:

*   `/`: The main landing page.
*   `/chat`: The chat interface for interacting with the AI.
*   `/journal`: A page for journaling.

## Backend

The backend is a FastAPI application located in the `backend` directory. It provides the following APIs:

*   `/api/quest/today`: Provides a daily quest to the user.
*   `/api/chat`: The main chat endpoint that interacts with the Gemini API to provide responses.

The backend uses the Gemini API for its conversational AI capabilities. It also uses a Firestore database, as suggested by the `seed_firestore.py` file.

# Building and Running

## Frontend

To run the frontend development server, navigate to the `frontend` directory and run:

```bash
npm install
npm run dev
```

To build the frontend for production, run:

```bash
npm run build
```

## Backend

To run the backend server, navigate to the `backend` directory and run:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend requires a `.env` file with a `GEMINI_API_KEY` to connect to the Gemini API.

# Development Conventions

*   **Frontend:** The frontend follows standard Next.js and React conventions. It uses TypeScript and Tailwind CSS.
*   **Backend:** The backend is a FastAPI application. It uses Pydantic for data validation and has a clear separation of concerns.
*   **API:** The API is documented in the `main.py` file, with clear request and response models.
