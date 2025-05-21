from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS setup for testing with any frontend or Soul Machines client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat_with_gpt(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input:
        return {"error": "No message received."}

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",  # Use gpt-3.5-turbo if needed
            messages=[
                {"role": "system", "content": "You are a helpful digital assistant with a friendly voice."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message["content"].strip()
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}