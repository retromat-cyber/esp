from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import openai
import os
import uvicorn
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

WAKE_WORD = "chatgpt"

# ======== /wake: принимает WAV, делает распознавание ========
@app.post("/wake")
async def wake_word_detect(file: UploadFile = File(...)):
    audio = await file.read()

    # Whisper model
    text = openai.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio, "audio/wav")
    ).text

    activated = WAKE_WORD.lower() in text.lower()

    return {"text": text, "wake": activated}

# ======== /chat: прокси ChatGPT ========
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[m.dict() for m in req.messages]
    )

    return JSONResponse(answer.choices[0].message.dict())

# ======== root ========
@app.get("/")
def home():
    return {"status": "ok", "message": "Wake + ChatGPT API ready"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000)
