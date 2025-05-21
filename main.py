from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# Serve HTML file from /static
app.mount("/", StaticFiles(directory="static", html=True), name="static")

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
        return {"message": {"type": "text", "content": "No message received."}}

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message["content"].strip()
        return {
            "message": {
                "type": "text",
                "content": reply
            }
        }
    except Exception as e:
        return {
            "message": {
                "type": "text",
                "content": f"Error: {str(e)}"
            }
        }
