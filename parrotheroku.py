import requests
import json
from flask import Flask, request

at = 'ZTczNGYyNjEtYWVhNi00N2UxLWJmOGUtMzBjNzkyODI5ZWNiNzU3ODg4OTgtMzNk'

# Init Flask
app = Flask(__name__)

# Helpers
def _url(path):
    return 'https://api.ciscospark.com/v1' + path

def _fix_at(at):
    if 'Bearer' not in at:
        return 'Bearer ' + at
    else:
        return at
        
# pySpark

def get_message(at, messageId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/messages/{:s}'.format(messageId)), headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    return message_dict

def post_message_markdown(at, text, roomId='', toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'markdown': text}
    if roomId:
        payload['roomId'] = roomId
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), json=payload, headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    return message_dict

        
# Bot functionality 
def parrot(input):
    text = "{}, {}".format(input, input)
    return text
    
def help():
    text = "Help Help!! I am the **parrot bot**. I repeat what you say."
    return text
    
def listen(input):
    if input.lower() == 'help':
        return help()
    else:
        return parrot(input)

"""
ENTRY FUNCTION FOR HEROKU
"""
@app.route('/', methods=['POST'])
def main():

# Get input info
    json_file = request.json
    resource = json_file['resource']
    event = json_file['event']
    data = json_file['data']

    # Check if the message came from the bot, if so, ignore
    person = data.get('personEmail')
    if person == 'aws_parrot@sparkbot.io':
        return
    
    # Get message contents
    msg_id = data.get('id')
    msg_dict = get_message(at, msg_id)
    #Parse the text
    input = msg_dict.get('text')
    if text: text = listen(input)
    
    # Get room information to send back to room the response
    #Parse the roomId
    room_id = data.get('roomId')
    
    # Send the spark message
    msg_dict = post_message_markdown(at, text, room_id)
    
    
    return message_dict['statuscode']
    
if __name__ == "__main__":
    app.run(debug=True)