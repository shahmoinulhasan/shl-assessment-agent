from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agent import get_agent_response

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Pass the conversation history to our Gemini agent
    raw_response = get_agent_response(request.messages)
    
    # Return it wrapped in the strict Pydantic model
    return ChatResponse(
        reply=raw_response["reply"],
        recommendations=raw_response["recommendations"],
        end_of_conversation=raw_response["end_of_conversation"]
    )