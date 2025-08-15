from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# AI স্ট্রিম জেনারেটর
def ai_stream(prompt: str):
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": True
    }

    with requests.post(url, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse("complibot.html", {"request": request})

# Streaming API (prompt form data নেবে)
@app.get("/stream")
def stream_response(prompt: str):
    return StreamingResponse(ai_stream(prompt), media_type="text/plain")
