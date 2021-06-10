
import json
import os
import uvicorn

import asyncio
from fastapi import FastAPI, Request, Header, BackgroundTasks

from aiolinebot import AioLineBotApi

from linebot import LineBotApi
from linebot.webhook import WebhookHandlerV2
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = FastAPI()

line_bot_api = AioLineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandlerV2(os.environ["LINE_CHANNEL_SECRET"])

num = 0

@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks, x_line_signature: str = Header(None)):

    body = await request.body()
    background_tasks.add_task(handles, body.decode("utf-8"), x_line_signature)

    return "ok"

async def handles(body, signature):
    await handler.handle_async(body, signature)

@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    global num
    num += 1
    print(num)
    await asyncio.sleep(20)
    await line_bot_api.push_message_async(event.source.user_id, TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
