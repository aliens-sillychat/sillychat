import asyncio
import os
from random import Random
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from .process import process_random_ban, process_random_blur_word, process_random_emoji

app = FastAPI()
connections: List[WebSocket] = []


MODIFICATION_PIPES = [
    process_random_blur_word,
    process_random_emoji,
    process_random_ban,
]

PROFILE_DIRECTORY = "static/profiles"
PROFILE_IMAGES = [
    file
    for file in map(
        lambda file: os.path.join(PROFILE_DIRECTORY, file), os.listdir("static/profiles")
    )
    if os.path.isfile(file) and file.endswith(".png")
]


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            message = await websocket.receive_json()
            await broadcast_message(message)
    except WebSocketDisconnect:
        pass

    connections.remove(websocket)


@app.get("/api/profiles/{id}")
async def random_profile(id: str):
    rand = Random()
    rand.seed(id)
    profile_image = rand.choice(PROFILE_IMAGES)
    return FileResponse(profile_image)


async def broadcast_message(message):
    before_messages = [message]
    after_messages = []

    for process in MODIFICATION_PIPES:
        for message in before_messages:
            processed_messages = process(message)
            after_messages += processed_messages

        before_messages = after_messages
        after_messages = []

    messages = before_messages

    for message in messages:
        await asyncio.gather(*[connection.send_json(message) for connection in connections])
