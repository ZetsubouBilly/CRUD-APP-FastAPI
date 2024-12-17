from typing import List
from fastapi import Body, FastAPI, status
from pydantic import BaseModel


app = FastAPI()


class Message(BaseModel):
    id: int = None
    text: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'text': 'Simple message',
                }
            ]
        }
    }


message_db = []


@app.get("/")
async def get_all_messages() -> List[Message]:
    return message_db


@app.get("/message/{message_id}")
async def get_message(message_id: int) -> Message:
    return message_db[message_id]


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if len(message_db) == 0:
        message.id = 0
    else:
        message.id = max([i.dict()['id'] for i in message_db]) + 1
    message_db.append(message)
    return 'Message created'


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    edit_message = message_db[message_id]
    edit_message.text = message
    return f'Message {message_id} updated'


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    message_db.pop(message_id)
    return f'Message {message_id} deleted'


@app.delete("/")
async def kill_message_all() -> str:
    message_db.clear()
    return "All messages deleted"