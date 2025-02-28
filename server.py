from fastapi import FastAPI
from mistralai import Mistral
from pydantic import BaseModel
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")
client = Mistral(api_key=api_key)

# Pydantic model for request
class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        chat_response = client.chat.complete(
            model=model,
            temperature=0.2,
            messages=[{"role": "user", "content": request.message}],
        )
        return {"response": chat_response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
