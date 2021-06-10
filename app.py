import responder
import json
import os

import time
import random

import asyncio

import logging.config

from aiolinebot import AioLineBotApi

from linebot import LineBotApi
from linebot.webhook import WebhookHandlerV2
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

api = responder.API()

line_bot_api = AioLineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandlerV2(os.environ["LINE_CHANNEL_SECRET"])

@api.route("/callback")
async def on_post(req, resp):
    @api.background.task
    async def handles(body, signature):
        await handler.handle_async(body, signature)

    signature = req.headers['X-Line-Signature']
    
    body = await req.media()
    body = json.dumps(body, ensure_ascii=False).replace(' ', '')

    try:
        resp.status_code = 200
        resp.text = 'OK'
        #TypeError: An asyncio.Future, a coroutine or an awaitable is required
        await handles(body, signature)
    except InvalidSignatureError as e:
        resp.status_code = 400
        resp.text = e


@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    await line_bot_api.reply_message_async(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))

    api.run(address='0.0.0.0', port=port, debug=True)