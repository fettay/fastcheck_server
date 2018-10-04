__author__ = 'raphaelfettaya'
import requests


URL = "http://localhost:5000/"


def send_message(sentence):
    data = {
        "object": "page",
        "entry": [
            {
                    "messaging": [
                        {
                        "message": {
                            "text": sentence
                        },
                        "sender": {
                            "id": 000
                        },
                    }
                ]
            }
        ]
    }
    response = requests.post(URL, json=data)

    return response


if __name__ == "__main__":
    while True:
        question = input("Enter a sentence")
        print()
        print(send_message(question).text)
