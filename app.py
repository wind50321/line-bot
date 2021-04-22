from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('WwjLdI3EW0S7++wjtGDtDh60uKUaxYLMr4Z22Ycu4sadqwWLRwfCSrMtE/zIBuw+JmQPd4/m1EJle4XtTofp0qe+kUPHcDbsDybYI28aCVhPobC/XzTQL4OOU+sgsVUHhdPkAeauvNs+ScGLkkTwugdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9c9e1e545965a880c9771655552dcc0f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，無法了解您的訊息'

    if '給我貼圖' in msg:
        sticker_msg = StickerSendMessage(
            package_id='11538',
            sticker_id='51626494'
        )
        line_bot_api.reply_message(
            event.reply_token,
            sticker_msg
        )
        return

    if msg in ['Hi', 'hi']:
        r = 'Hello'
    elif msg == '你吃飯了嗎':
        r = '還沒喔'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r)
    )


if __name__ == "__main__":
    app.run()