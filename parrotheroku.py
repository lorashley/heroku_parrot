import requests
import json
import os
from flask import Flask, render_template, request

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

@app.route('/', methods=['GET'])
def landing():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def main():

    username = os.environ.get('SPARK_BOT_USERNAME')
    #print("Username from environment: {}".format(username))
    
    at = os.environ.get('SPARK_BOT_AUTH_TOKEN')
    #print("auth: {}".format(at))
    # Get input info
    json_file = request.json
    resource = json_file['resource']
    event = json_file['event']
    data = json_file['data']

    # Check if the message came from the bot, if so, ignore
    person = data.get('personEmail')
    if '@webex.bot' not in username:
        bot_name = username + '@webex.bot'
    else:
        bot_name = username
    if person == bot_name:
        return 'heroku done', 200
    
    # Get message contents
    msg_id = data.get('id')
    msg_dict = get_message(at, msg_id)
    #Parse the text
    input = msg_dict.get('text')
    if input: 
        text = listen(input)
    else:
        return 'heroku done', 200
    
    # Get room information to send back to room the response
    #Parse the roomId
    room_id = data.get('roomId')
    
    # Send the spark message
    
    msg_dict = post_message_markdown(at, text, room_id)
    return msg_dict['statuscode']
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
