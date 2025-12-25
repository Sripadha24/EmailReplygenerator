from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Get Gemini API key from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Request model for email generation
class EmailRequest(BaseModel):
    email_situation: str
    tone: str  # formal, semi-formal, friendly

# Response model for generated email
class EmailResponse(BaseModel):
    reply: str

@api_router.get("/")
async def root():
    return {"message": "Email Reply Generator API"}

@api_router.post("/generate-reply", response_model=EmailResponse)
async def generate_email_reply(request: EmailRequest):
    """
    Generate a professional email reply using Gemini AI.
    Accepts email situation and tone, returns only the email body text.
    """
    # Validate input
    if not request.email_situation or request.email_situation.strip() == "":
        raise HTTPException(status_code=400, detail="Email situation cannot be empty")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    
    # Map tone to description for the prompt
    tone_descriptions = {
        "formal": "formal and professional",
        "semi-formal": "semi-formal and polite but approachable",
        "friendly": "friendly and warm while remaining professional"
    }
    
    tone_desc = tone_descriptions.get(request.tone, "professional")
    
    # Construct the prompt for Gemini
    system_message = f"""You are an expert email writer. Generate a {tone_desc} email reply based on the situation provided.

Rules:
- Only output the email body text, no subject line
- Do not include greetings like "Dear [Name]" unless specifically needed
- Do not include closing signatures like "Best regards, [Name]"
- Keep the response concise and to the point
- Maintain the specified tone throughout
- Be polite and professional regardless of the tone selected"""

    user_prompt = f"Write a {tone_desc} email reply for this situation:\n\n{request.email_situation}"
    
    try:
        # Initialize Gemini chat
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id="email-reply-generator",
            system_message=system_message
        ).with_model("gemini", "gemini-2.5-flash")
        
        # Create and send message
        user_message = UserMessage(text=user_prompt)
        response = await chat.send_message(user_message)
        
        return EmailResponse(reply=response.strip())
        
    except Exception as e:
        logging.error(f"Error generating email reply: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate email reply. Please try again.")

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
