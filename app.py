import flask
from we import WeaG

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = flask.Flask(__name__)
w = WeaG() 

# 用您的 Channel Access Token 和 Channel Secret 替換以下值
line_bot_api = LineBotApi('OHHU5/3aJTGfZ2GaIWK0WGszIVBvRAagAhCjAOD9RWOpw42AvkQv38Bt7aXdKBadTEpcg526bReSZr9AS2zyE4kFMUWxNt3Ye1jf0ubJbjPLJm3VItqtHbvd9Fsi06sXWtimw+U0aPrykSDNChQMQgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b7c0a3e497c95a20ab0d62288110625a')

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']

    # 獲取請求體
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    site = event.message.text
    info = w.grab(site)
    if not info:
        info = '查無資料'
    else:
        info = w.tostr(info)


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=info)
    )

if __name__ == "__main__":
    app.debug = True
    app.run()





# @app.route('/weather' , methods=['GET' , 'POST'])  #json
# def weather():
#     r = {}
    
#     if site :=flask.request.json.get('site'): #if site :
#         r = w.grab(site)
#     return r