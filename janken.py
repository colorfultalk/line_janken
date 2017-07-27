# coding: UTF-8
from flask import Flask, request, abort
from linebot import (
  LineBotApi, WebhookHandler
)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage,
)
import os, random

# user defined modules
from models import Player, db
# user define constants
ROCK     = 100
PAPER    = 200
SCISSORS = 300
HANDS    = [ROCK, PAPER, SCISSORS]

app = Flask(__name__)
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

def before_request_handler():
  db.connect()

def after_request_handler():
  db.close()

def playJanken(playerHand):
    enemyHand = random.choice(HANDS)
    if enemyHand == playerHand:
        return "draw"
    if enemyHand == ROCK and playerHand == PAPER:
        return "win"
    elif enemyHand == PAPER and playerHand == SCISSORS:
        return "win"
    elif enemyHand == SCISSORS and playerHand == ROCK:
        return "win"
    else:
        return "lose"

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
  query = Player.select().where(Player.lineId == uId)
  # if player is new
  if not( query.exists() ):
    # save Player
    player = Player(lineId = uId, displayName = name)
    player.save()
    print( "player saved!" )
  else:
    player = query.get()
    win = player.win
    lose = player.lose
    print( "win:" + str(win) )

  # store user's text
  text = event.message.text
  print( text )

  if text == u'ぐー':
      playerHand = ROCK
      judge = playJanken(playerHand)
      if judge == "win":
          reply_text = "you win"
      elif judge == "lose":
          reply_text = "you lose"
      else:
          reply_text = "draw"
      # reply
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
      )
  else:
    # reply
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
  app.run()

