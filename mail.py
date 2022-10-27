import requests

url = 'https://cfm7773.uta.cloud/sendEmail.php'

def send_email(email, text):
    #demonstrate how to use the 'params' parameter:
    x = requests.get(url, params = {"email": email, "text": text})

    #print the response (the content of the requested file):
    print(x.text)
    return True