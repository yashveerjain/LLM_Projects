from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from ml_utils.rag import RAG
from ml_utils.llm_handler import LLMHandler


llm = LLMHandler()

# Load environment variables
load_dotenv()

# Get the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your Next.js app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# vector store path
vector_store_dir = "db"
os.makedirs(vector_store_dir, exist_ok=True)

vector_store_file = os.path.join(vector_store_dir, "chroma.db") # "chroma.db"
# if os.path.exists(vector_store_file) : shutil.rmtree(vector_store_file) 
from ml_utils.rag import RAG

rag = RAG(vector_store_file, "headstarter_policy")

rag.add_url("https://headstarter.co/privacy-policy")
rag.add_url("https://headstarter.co/info")


# # Configure Gemini API (replace with your actual API key)
# genai.configure(api_key=GEMINI_API_KEY)

# System instructions
SYSTEM_INSTRUCTIONS = """
You are Headstarter's Tech Support Bot, a knowledgeable assistant for Headstarter AI's community of emerging software engineers. Your role is to help users with technical issues, provide information about Headstarter's programs, and offer guidance on career development in software engineering. Give clear, concise, and friendly responses. If you can't resolve an issue, direct the user to human support. If the user doesn't input anything, politely ask if they still need assistance. Don't add any emojis. Let's get started!
"""

# Create a model instance
# model = genai.GenerativeModel('gemini-1.5-flash')

llm.updade_prompt(SYSTEM_INSTRUCTIONS)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        
        # RAG
        message = request.message
        context = rag.get_context(message)
        print("message : ", message)
        print("context : ", context)
        # Send user message and get response
        response = llm.get_response(message, rag_context=context)
        
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Headstarter Tech Support Bot API. Use the /chat endpoint to chat."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)