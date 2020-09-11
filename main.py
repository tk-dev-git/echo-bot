from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os
import template.message_ysdm as ysdm
import template.message_ymst as ymst

app=Flask(__name__)

#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN=os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET=os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body: {}".format(body))

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    flex_ysdm = FlexSendMessage.new_from_json_dict(ysdm.get_ysdm_message())
    flex_ymst = FlexSendMessage.new_from_json_dict(ymst.get_message_ymst())
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    line_bot_api.reply_message(event.reply_token, messages=[flex_ysdm, flex_ymst])

if __name__=="__main__":
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
