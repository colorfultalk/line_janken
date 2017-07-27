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

def judgeJanken(playerHand):
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

def playJanken(playerHand):
    judge = judgeJanken(playerHand)

    if judge == "win":
        reply_text = "you win"
    elif judge == "lose":
        reply_text = "you lose"
    else:
        reply_text = "draw"

    return reply_text

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

  # store user's text
  text = event.message.text
  print( text )

  # play janken
  if text == u'ぐー':
      playerHand = ROCK
      reply_text = playJanken(playerHand)
      # reply
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
      )
  elif text == u'ちょき':
      playerHand = SCISSORS
      reply_text = playJanken(playerHand)
      # reply
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
      )
  elif text == u'ぱー':
      playerHand = PAPER
      reply_text = playJanken(playerHand)
      # reply
      line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
      )
  else:
    win = player.win
    reply_text = "win:" + str(win)
    # reply
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

  if reply_text == "you win":
      win = player.win
      player.win = win + 1
      player.save()

if __name__ == "__main__":
  app.run()

