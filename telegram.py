import requests

url = 'https://api.telegram.org:443/bot5651343058:AAEM0OVxht0AkvJk5RLQ4JJfm7dbuB0qawQ/sendMessage'

def send_message(user_id, text):
    #demonstrate how to use the 'params' parameter:
    x = requests.get(url, params = {"chat_id": user_id, "text": text, "parse_mode": "MarkdownV2"})

    #print the response (the content of the requested file):
    return True