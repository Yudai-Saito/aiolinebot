import responder
import json
import os

import time
import random

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


api = responder.API()

line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

num = 0

@api.route("/callback")
async def on_post(req, resp):
    @api.background.task
    def handles():
        handler.handle(body, signature)

    signature = req.headers['X-Line-Signature']
    
    body = await req.media()
    body = json.dumps(body, ensure_ascii=False).replace(' ', '')

    try:
        handles()
        resp.status_code = 200
        resp.text = 'OK'
    except InvalidSignatureError as e:
        print(e)
        resp.status_code = 400
        resp.text = e


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global num
    num += 1
    print(num)
    time.sleep(20) 
    line_bot_api.push_message(event.source.user_id, TextSendMessage(event.message.text))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    api.run(address='0.0.0.0', port=port, debug=True)