import os, sys, json, requests
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAhLsI2qzIsBAIZA15hZBTf6ox15MjrYhSHeU3jFWZCZAA89aHO0DZBFnoMB5FIRtFnIUaFo8mTc2vA9cgKnEO5FfE7mChtPVh16JVPA0oJ9LTUnVtjwt4txNi7dGqkOuFSZBs3PvAyamWaIFTAL1tYqHAx0HmSMSaSa08WMmlGe3u7CHpZAxRn"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "Sl33pyW00ly"

@app.route('/', methods=['GET'])
def verify():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "WEBHOOK VERIFIED", 200

"""
def getValues(sender_psid):
    URL = "https://graph.facebook.com/"+sender_psid+"?fields=first_name,last_name,profile_pic&access_token="+PAGE_ACCESS_TOKEN
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user = requests.get(url = URL, params=user_details_params).json
    print(user)
    first_name = user['first_name']
    last_name = user['last_name']

//not included
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 

    user_details = requests.get(user_details_url, user_details_params).json() 
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
    """

@app.route('/', methods=['POST'])
def webhook():
    print(request.data)
    data = request.get_json()

    if data['object'] == "page":
        entries = data['entry']

        for entry in entries:
	        messaging = entry['messaging']
			
        for messaging_event in messaging:
            sender_psid = messaging_event['sender']['id']
            recipient_psid = messaging_event['recipient']['id']
            getValues(sender_psid)

        if messaging_event.get('message'):
            message_hook = messaging_event.get('message')
            handleMessage(sender_psid, message_hook)
        elif messaging_event.get('postback'):
            handlePostback(sender_psid, messaging_event.get('postback'))

        return "ok", 200
    else:
        #Return a '404 Not Found' if event is not from a page subscription
        return "error", 404

#Handles messages events
def handleMessage(sender_psid, received_message):
    #HANDLES REGULAR TEXT
    if received_message.get('text'):
        response = "Welcome to Scholarly"

    callSendAPI(sender_psid, response)

#Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback):
    test = "thanks for being here"


# Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {"id": sender_psid},
                    "message": {"text": response}})

    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token=EAAhLsI2qzIsBAIZA15hZBTf6ox15MjrYhSHeU3jFWZCZAA89aHO0DZBFnoMB5FIRtFnIUaFo8mTc2vA9cgKnEO5FfE7mChtPVh16JVPA0oJ9LTUnVtjwt4txNi7dGqkOuFSZBs3PvAyamWaIFTAL1tYqHAx0HmSMSaSa08WMmlGe3u7CHpZAxRn", headers=headers, data=data)
    print (r.text)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)



def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)