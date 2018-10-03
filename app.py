__author__ = 'raphaelfettaya'

import os
import json
import requests
from flask import Flask, request
from pymessenger.bot import Bot
import logging

app = Flask(__name__)
BOT = Bot(os.environ["ACCESS_TOKEN"])
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
    logger.debug(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        response_text = 'ABC'

                        if 'DEBUG' in os.environ:
                            logger.debug(response_text)
                            return response_text, 200

                        BOT.send_message(sender_id, response_text)
                    except Exception:
                        BOT.send_message(sender_id, 'MISS')
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
  except Exception as e:
    logger.exception(e)


def send_message(recipient_id, message_text):

    logger.debug("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        logger.error(r.status_code)
        logger.error(r.text)


if __name__ == '__main__':
    app.run(debug=True)