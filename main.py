from flask import Flask, render_template, request
from mysql import check_email, check_tid, check_tempotid, insert_tempouser, get_tempostatus, update_tempostatus, \
    update_tempocode, get_tempocode, delete_tempouser, update_tempoemail, update_status, update_tid, get_tempoemail
from telegram import send_message
from mail import send_email
import random

app = Flask(__name__)

@app.route('/', methods = ['POST'])

def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    user_id = request.form['id']
    user_message = request.form['message']
    if check_tid(user_id):
        send_message(user_id, "yes")
    else:
        if check_tempotid(user_id):
            tempo_status = get_tempostatus(user_id)
            if tempo_status == 1:
                if check_email(user_message):
                    code = random.randint(1000,9999)
                    send_email(user_message, code)
                    update_tempostatus(user_id, 2)
                    update_tempocode(user_id, code)
                    update_tempoemail(user_id, user_message)
                    send_message(user_id, '__LOGIN__ \-\> Provide the code sent to email')
                else:
                    send_message(user_id, '__LOGIN__ \-\> Email not found')
                    delete_tempouser(user_id)
            if tempo_status == 2:
                if str(get_tempocode(user_id)) == user_message:
                    print(get_tempoemail(user_id))
                    update_tid(user_id, get_tempoemail(user_id))
                    update_status(user_id, 1)
                    delete_tempouser(user_id)
                    send_message(user_id, '__VTA__ \-\> Welcome')
                else:
                    send_message(user_id, '__LOGIN__ \-\> Code not correct')
                    delete_tempouser(user_id)
        else:
            print(insert_tempouser(user_id))
            send_message(user_id, '__LOGIN__ \-\> Provide your UTA email')
    return render_template('index.html', userm=user_message)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)