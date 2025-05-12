import os
import re
import json
import base64
import uvicorn
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Header

load_dotenv()

Funny_KEY = os.getenv("secret_laugh")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

port = int(os.environ.get('PORT', 8080))

app.mount("/public/static", StaticFiles(directory="public/static"), name="static")

@app.get("/get-jokes-from-user")
async def get_some_jokes(authorization: str = Header(None)):
    if authorization != f"Bearer {Funny_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return FileResponse("game_time_jokes.json")
    
@app.post("/crack_some_jokes")
async def store_user(request: Request):
    data = await request.json()  # <-- await here, because it's an async method

    # Store to file
    with open("game_time_jokes.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    return JSONResponse({"status": "success", "received": data})


@app.get("/")
async def serve_homepage():
    return FileResponse("index.html")

@app.get("/laugh")
async def serve_funnypage():
    return FileResponse("/public/templates/laugh.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
