import requests

url = 'https://api.telegram.org:443/bot5651343058:AAEM0OVxht0AkvJk5RLQ4JJfm7dbuB0qawQ/sendMessage'

def send_message(user_id, text):
    #demonstrate how to use the 'params' parameter:
    # x = requests.get(url, params = {"chat_id": user_id, "text": text, "parse_mode": "MarkdownV2"})

    myobj = {
             "chat_id": user_id,
             "text": text,
             "parse_mode": "MarkdownV2",
             "reply_markup": {}
             }

    x = requests.post(url, json=myobj)

    #print the response (the content of the requested file):
    print(x.text)
    return True


def send_message_with_reply(user_id, text, buttons):
    # demonstrate how to use the 'params' parameter:
    # x = requests.get(url, params = {"chat_id": user_id, "text": text, "parse_mode": "MarkdownV2"})

    myobj = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "MarkdownV2",
        "reply_markup": {
            "keyboard": buttons,
            "resize_keyboard": True,
            "one_time_keyboard": True,
            "input_field_placeholder": "Select one option:"
        }

    }

    x = requests.post(url, json=myobj)

    # print the response (the content of the requested file):
    print(x.text)
    return True