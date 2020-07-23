import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "A4H7CGJUUGCPBKHFNB5ZBKIVLNYJVICX"
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
                        response = "Ok. You're in the right place! I will send you {0}".format(str(value))
                    if entity ==   "institution":
                        response = "Great. I've heard that {0} is a great institution".format(str(value))  
                    if entity == "degree_program":
                        response = "Awesome! One step closer to getting that dream job!"  
                    if entity == "year_of_study":
                        response = "We at Scholarly are proud of you for starting your higher education journey"  
                    if entity == "closing":
                        response = "Bye. All the best!"        
                    if entity == "wit/greetings":
                        response = "Welcome to Scholarly!"
                    if entity == "wit/thanks":
                        response = "Thank-you"        
                    elif entity == "wit_field_of_study":
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