# Email Reply Generator - Requirements & Architecture

## Original Problem Statement
Build a simple, clean web application called "Email Reply Generator" that generates professional email replies using Google Gemini AI based on user input.

## User Choices
- **AI Integration**: User's own Google Gemini API key
- **Theme**: Dark mode
- **Backend**: FastAPI (Python)

## Architecture

### Tech Stack
- **Frontend**: React with Tailwind CSS, Shadcn UI components
- **Backend**: FastAPI (Python) with emergentintegrations library
- **AI**: Google Gemini 2.5 Flash model
- **No Database**: Stateless application

### Key Files
- `/app/backend/server.py` - FastAPI backend with `/api/generate-reply` endpoint
- `/app/frontend/src/App.js` - React frontend single-page app
- `/app/frontend/src/App.css` - Custom dark theme styles
- `/app/frontend/src/index.css` - Global styles with Outfit/Inter fonts

### API Endpoints
- `GET /api/` - Health check
- `POST /api/generate-reply` - Generate email reply
  - Request: `{ email_situation: string, tone: "formal" | "semi-formal" | "friendly" }`
  - Response: `{ reply: string }`

## Features Implemented
1. ✅ Email situation textarea input
2. ✅ Tone selection dropdown (Formal, Semi-formal, Friendly)
3. ✅ Generate Reply button with loading state
4. ✅ Generated reply display area
5. ✅ Copy to Clipboard functionality
6. ✅ Empty input validation with toast notifications
7. ✅ Dark theme with glassmorphism effects
8. ✅ Responsive design

## Next Action Items
- Add keyboard shortcuts (Ctrl+Enter to generate)
- Add reply length options (short, medium, long)
- Add history feature to save recent generations
- Add export options (save as .txt, email directly)

## How to Run Locally
1. Set GEMINI_API_KEY in `/app/backend/.env`
2. Backend runs on port 8001 (FastAPI)
3. Frontend runs on port 3000 (React)
