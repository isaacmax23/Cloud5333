# import requests
# import smtplib, ssl, os, base64, json


# def send_email(event,context):
#   url = 'https://cfm7773.uta.cloud/sendEmail.php'
#   request = json.loads(base64.b64decode(event['data']).decode('utf-8'))
#   email=request.get('email')
#   text=request.get('text')
#   print(text)
#   x = requests.get(url, params = {"email":email, "text":text})
#   print(x.status_code)
#   return True

import smtplib, ssl, os, base64, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Supply these via Environment Variables in the Cloud Function

SMTP_SERVER = os.environ.get('SMTP_SERVER')

SMTP_PORT = os.environ.get('SMTP_PORT')

SENDER_EMAIL = os.environ.get('SENDER_EMAIL')

SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
def build_message(request):
  receiver_email = request.get('receiver_email')
  subject = request.get('subject')
  text = MIMEText(request.get('message'), "plain")
        # html = MIMEText(html, 'html')
  message = MIMEMultipart("alternative")
  message["Subject"] = subject
  message["From"] = SENDER_EMAIL
  message["To"] = receiver_email
  message.attach(text)
  print("message",message)
  return message



def send_tls(event, context):
# print(event)
  request = json.loads(base64.b64decode(event['data']).decode('utf-8'))
  # print(request)
  ssl_context = ssl.create_default_context()
  ssl_context.check_hostname = False
  message = build_message(request=request)
  print("here")  
  with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as server:
    print("in")
    server.connect(host=SMTP_SERVER, port=SMTP_PORT) # seems redundant, but accommodates a bug in smtplib
    print("connected")
    server.starttls(context=ssl_context)
    print("tls")
    server.login(user=message.get('From'),password=SENDER_PASSWORD)
    print("successful Login")
    server.sendmail(from_addr=message.get('From'), to_addrs=message.get('To'), msg=message.as_string())
    print("here22")
  
