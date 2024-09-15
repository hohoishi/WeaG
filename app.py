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
line_bot_api = LineBotApi('123123')
handler = WebhookHandler('123123')

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