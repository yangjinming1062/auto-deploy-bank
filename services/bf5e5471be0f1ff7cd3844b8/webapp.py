#!/usr/bin/env python3
"""
Simple web interface for ChatDB
"""
import threading
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chatdb import generate_chat_responses, init_database, database_info
from mysql import MySQLDB
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Global database connection
mysql_db = None
his_msgs = []

def init_mysql():
    global mysql_db
    try:
        mysql_db = init_database(database_info, "try1024")
        return True
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
        return False

# Initialize database in background
init_thread = threading.Thread(target=init_mysql)
init_thread.start()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected" if mysql_db else "initializing"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input:
        return {"error": "No message provided"}

    try:
        generate_chat_responses(user_input, mysql_db, his_msgs)
        return {"response": "Response generated - check logs for details"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("WEB_PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)