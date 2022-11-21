from flask import Flask, render_template, request, current_app
from mysql import check_email, check_tid, check_tempotid, insert_tempouser, get_tempostatus, update_tempostatus, \
    update_tempocode, get_tempocode, delete_tempouser, update_tempoemail, update_status, update_tid, get_tempoemail
from telegram import send_message
from mail import send_email
import random
import json
from google.cloud import pubsub_v1



app = Flask(__name__)

@app.get("/")
def index():
    project_id = "top-cubist-365802"
    topic_id = "otp-email-list"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    x = {
            "email": "isaac@cfm7773.uta.cloud",
            "text": "Isaac got the message"
        }
    data_str = json.dumps(x)
    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    future1 = publisher.publish(topic_path, data)
    print(future1.result())
    return "Hello World!\n"
if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)


