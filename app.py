__author__ = 'raphaelfettaya'

import os
from flask import Flask, request
from pymessenger.bot import Bot
from logic import answer
from logger import get_logger


#if 'DEBUG' not in os.environ:
os.system('python -m spacy download en_core_web_sm')


app = Flask(__name__)
BOT = Bot(os.environ["ACCESS_TOKEN"])
logger = get_logger(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
  try:
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        logger.info('Question: ' + message_text)
                        response_text = answer(message_text)
                        logger.info('Answer: ' + response_text)

                        if 'DEBUG' in os.environ:
                            return response_text, 200

                        BOT.send_text_message(sender_id, response_text)
                    except Exception as e:
                        logger.exception(e)

                        if 'DEBUG' in os.environ:
                            return 'MISS', 200

                        BOT.send_text_message(sender_id, 'MISS')

    return "ok", 200
  except Exception as e:
    logger.exception(e)

if __name__ == '__main__':
    app.run(debug=True)
