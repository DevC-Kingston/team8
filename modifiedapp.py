import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAhLsI2qzIsBAHHFK3JZByCi4nCrZBbMMCFAHj60lm65swCO8cliQ5ZB72PJSsZAx2QYyaCH2OgwZAwOSj3KN8yjOZA76ZCSBsRFUpd2xmz9cVGZBJhhxNAi4RjZCZAeLj4YYnP0zbdcP91n6pcz4B5h5OMnQfwwrSAJYpmZBqLOObrBQZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

#VERIFICATION_TOKEN = "Sl33pyW00ly"

@app.route('/', methods=['GET'])
def verify():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "WEBHOOK VERIFIED", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                #IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:    
                        messaging_text = 'no text'

                    response = None 

                    entity, value = wit_response(message) 

                    if entity == "scholarship": 
                        response = "Ok. You're in the right place! I will send you {} scholarships".format(str(value))
                    elif entity == "field_of_study":
                        response =  "Awesome! So you're studying {0}. All the best the field of {0}".format(str(value))

                    if entity ==  None:
                        response = "Sorry I didn't understand"  
                    bot.send_text_message(sender_id, response)    

    return "Ok", 200

def log(message):
    print(message)
    sys.stdout.flush()
    
if __name__ == "__main__":
    app.run(debug = True, port = 80)