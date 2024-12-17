from typing import List
from fastapi import Body, FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Message(BaseModel):
    id: int = None
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Simple message",
                }
            ]
        }
    }


message_db = []


@app.get("/")
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "message.html", {"request": request, "messages": message_db}
    )


@app.get("/message/{message_id}")
async def get_message(request: Request, message_id: int) -> Message:
    try:
        return templates.TemplateResponse(
            "message.html", {"request": request, "message": message_db[message_id]}
        )
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if len(message_db) == 0:
        message.id = 0
    else:
        message.id = max([i.dict()["id"] for i in message_db]) + 1
    message_db.append(message)
    return "Message created"


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = message_db[message_id]
        edit_message.text = message
        return f"Message {message_id} updated"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        message_db.pop(message_id)
        return f"Message {message_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
async def kill_message_all() -> str:
    message_db.clear()
    return "All messages deleted"
