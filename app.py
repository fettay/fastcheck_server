__author__ = 'raphaelfettaya'

import os
from flask import Flask, request
from pymessenger.bot import Bot
from logic import answer, ExtractionError
from logger import get_logger
import threading



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


def process_request(data):
    # data = request.get_json()
    pass



@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
  try:
    data = request.get_json()

    # threading.Thread(target=process_request, args=data).start()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    BOT.send_text_message(sender_id, "That is a great question, I am checking it")
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        if message_text == "True" or message_text == "False":
                            return "ok", 200
                    
                        logger.info('Question: ' + message_text)
                        response_text = answer(message_text)
                        logger.info('Answer: ' + response_text)

                        if 'DEBUG' in os.environ:
                            return response_text, 200

                        BOT.send_text_message(sender_id, response_text)
                    except ExtractionError:
                        BOT.send_text_message(sender_id, "I cannot answer to this")

                    except Exception as e:
                        logger.exception(e)

                        if 'DEBUG' in os.environ:
                            return 'MISS', 200

                        BOT.send_text_message(sender_id, "I'm ill a little bit")


    return "ok", 200
  except Exception as e:
    logger.exception(e)
    return "Error", 400


@app.route('/api', methods=['POST'])
def alexa_api():
    try:
        data = request.get_json()
        logger.debug('Got request from Alexa:')
        logger.debug(data)
        text = data["message"]

        try:
            response_text = answer(text)
        except Exception as e:
            logger.exception(e)
            response_text = "I cannot find any answer to that"

        logger.debug('Question: ' + text)
        logger.debug('Answer: ' + response_text)
        return response_text, 200

    except Exception:
        return "Missed", 400

if __name__ == '__main__':
    app.run(debug=True)
