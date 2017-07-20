from flask import Flask, request, abort
from linebot import (
  LineBotApi, WebhookHandler
)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage,
)
import os

# user defined modules
from models import Player

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

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
    abort(400)

  return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  # get user_id from event
  uId = event.source.user_id
  profile = line_bot_api.get_profile(uId)
  name = profile.display_name

  # query player with uId
  thisPlayer = Player.query.filter_by(lineId=uId).first()
  # if player is new
  if thisPlayer is none:
    # save Player
    player = Player(lineId = uId, displayName = name)
    player.save()
    print( "player saved!" )
  else:
    win = thisPlayer.win
    lose = thisPlayer.lose
    print( "win:" + str(win) )


  # reply
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text)
  )

if __name__ == "__main__":
  app.run()

