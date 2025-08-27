

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
from typing import Optional

import ai
from ai import ChatManager
from random import randint
import time




app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


logger = logging.getLogger('logger')
chatManager = ChatManager()


# Pydantic models for request bodies
class ChatMessage(BaseModel):
    message: str
    chat_id: int


class ResetRequest(BaseModel):
    message: Optional[str] = ""


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/twenty_q", response_class=HTMLResponse)
async def twenty_q(request: Request):
    chat_count = await chatManager.chat_count()
    print("CHATS", chat_count)
    return templates.TemplateResponse("twenty_q.html", {"request": request})


@app.post("/start_chat")
async def start_chat():
    chat_id = await chatManager.add_chat()
    reply = await chatManager.start_chat(global_id=chat_id)
    print("START CHAT", chat_id)

    # Log conversation
    convo = await chatManager.get_convo(chat_id)
    for x in convo:
        print(x)
        print("\n")

    return {
        'reply': reply,
        'chat_id': chat_id
    }


@app.post("/chat")
async def chat(chat_data: ChatMessage):
    print(f'Chat() Chat id: {chat_data.chat_id}')
    print(f'Chat Mgr id: {chatManager.__hash__()}')

    reply = await chatManager.send_chat(
        global_id=chat_data.chat_id,
        user_message=chat_data.message
    )

    return {'reply': reply}


@app.post("/reset_chats")  # Changed to POST since it modifies state
async def reset_chats():
    await chatManager.clear_all_chats()
    ct = await chatManager.chat_count()
    return {'reply': f'Chats reset: counter {ct}'}


# Alternative GET version if you need it
@app.get("/reset_chats")
async def reset_chats_get():
    await chatManager.clear_all_chats()
    ct = await chatManager.chat_count()
    return {'reply': f'Chats reset: counter {ct}'}


if __name__ == "__main__":
    import  uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)