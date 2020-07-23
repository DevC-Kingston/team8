import os, sys, json, requests
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "A4H7CGJUUGCPBKHFNB5ZBKIVLNYJVICX"

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
    getstarted()

def getstarted():
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"get_started": {"payload": "GET_STARTED_PAYLOAD"}})
    r = requests.post('https://graph.facebook.com/v7.0/me/messenger_profile?access_token='+ PAGE_ACCESS_TOKEN, headers=headers, data=data)


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

        #Handles messages events
        if messaging_event.get('message'):
            if 'text' in messaging_event['message']:
                messaging_text = messaging_event['message']['text']
                if 'Hey' in  messaging_text:
                    response = "Welcome to Scholarly. Where the scholarships island wide are placed in a easy to access way for all university students."
                    response2 = "Please Select your year."
                    callSendAPI_TextMessage(sender_psid, response)
                    callSendAPI_QuickReply(sender_psid, response2)  
                if 'Year 1' in messaging_text: 
                    response = "Excellect !"
                    callSendAPI_TextMessage(sender_psid, response)
                    response2 = "Major ?."
                    callSendAPI_QuickReplyDegree(sender_psid, response2)
                if 'Year 2' in messaging_text:
                    response = "Excellect !"
                    callSendAPI_TextMessage(sender_psid, response)
                    response2 = "Major ?."
                    callSendAPI_QuickReplyDegree(sender_psid, response2)
                if 'Computer Scinece' in messaging_text:
                    response = "That's amazing ! 1's and 0's are the way of life !"
                    callSendAPI_TextMessage(sender_psid, response)
                    response2 = "Institution ?"
                    callSendAPI_QuickReplySch(sender_psid, response2)
                if 'UTECH' in messaging_text:
                    response = "Thank you.. Please give us a sec"
                    callSendAPI_TextMessage(sender_psid, response)
                    response = "Computing results..."
                    callSendAPI_TextMessage(sender_psid, response)
                #witAI
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
                callSendAPI_TextMessage(sender_psid, response)
                    
        elif messaging_event.get('postback'):
            handlePostback(sender_psid, messaging_event.get('postback'))

        return "ok", 200
    else:
        #Return a '404 Not Found' if event is not from a page subscription
        return "error", 404

def degreeOpt(sender_psid):
    reply_tester = "Whats your degree ?"
    callSendAPI_TextMessage(sender_psid, reply_tester)


#Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback):
    test = "thanks for being here"

# Sends response messages via the Send API
def callSendAPI_TextMessage(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {"id": sender_psid},
                    "message": {"text": response}})

    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
    print (r.text)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


# Sends response quick reply messages via the Send API
def callSendAPI_QuickReply(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {
            "id": sender_psid
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": response,
            "quick_replies":[
            {
                    "content_type":"text",
                    "title":"Year 1",
                    "payload":"year1",
                },
                {
                    "content_type":"text",
                    "title":"Year 2",
                    "payload":"year2",                      
                },
                {
                    "content_type":"text",
                    "title":"Year 3",
                    "payload":"year3",
                },
                {
                    "content_type":"text",
                    "title":"Final Year",
                    "payload":"final",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

# Sends response quick reply messages via the Send API
def callSendAPI_QuickReplyDegree(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {
            "id": sender_psid
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": response,
            "quick_replies":[
            {
                    "content_type":"text",
                    "title":"Ccomputer Science",
                    "payload":"computerScince",
                },
                {
                    "content_type":"text",
                    "title":"Law",
                    "payload":"law",                      
                },
                {
                    "content_type":"text",
                    "title":"Accounting",
                    "payload":"year3",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


# Sends response quick reply messages via the Send API
def callSendAPI_QuickReplySch(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient": {
            "id": sender_psid
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": response,
            "quick_replies":[
            {
                    "content_type":"text",
                    "title":"UTECH",
                    "payload":"utech",
                },
                {
                    "content_type":"text",
                    "title":"UWI",
                    "payload":"uwi",                      
                },
                {
                    "content_type":"text",
                    "title":"NCU",
                    "payload":"ncu",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


# Sends response template messages via the Send API
def callSendAPI_templateDegree(sender_psid):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient":{
            "id":sender_psid
        },
        "message":{
            "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements":[
                {
                    "title":"Computer Science",
                    "image_url":"https://apprecs.org/gp/images/app-icons/300/4f/com.utech.sapna.utechapp.jpg",
                    "subtitle":"Where machine and human combine",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"Definitely !",
                        "payload":"computer_science"
                    }              
                    ]      
                },
                {
                    "title":"Law",
                    "image_url":"https://cdn.pixabay.com/photo/2018/03/28/06/42/lawyer-3268430_960_720.jpg",
                    "subtitle":"Helping, Protecting & Serving",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"Definitely !",
                        "payload":"law"
                    }              
                    ]      
                },
                {
                    "title":"Accounting",
                    "image_url":"https://blog.hubspot.com/hubfs/Sales_Blog/small-business-accounting-software.jpg",
                    "subtitle":"Numbers, numbers, numbers !",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"Definitely !",
                        "payload":"accounting"
                    }              
                    ]      
                }
                ]
            }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def callSendAPI_templateSchool(sender_psid):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "recipient":{
            "id":sender_psid
        },
        "message":{
            "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements":[
                {
                    "title":"Utech",
                    "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTqzy03QJoSeuOpx-Rzw2ngkUw9nDNjYwxkKA&usqp=CAU",
                    "subtitle":"Excellence Through Knowledge",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"Utech Knight",
                        "payload":"utech"
                    }              
                    ]      
                },
                {
                    "title":"UWI",
                    "image_url":"https://upload.wikimedia.org/wikipedia/commons/6/62/UWILogotype.jpg",
                    "subtitle":"Light rising from the West",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"UWI",
                        "payload":"uwi"
                    }              
                    ]      
                },
                                {
                    "title":"NCU",
                    "image_url":"https://fiwibusiness.com/wp-content/uploads/2016/07/NCU_LOGO.jpg",
                    "subtitle":"Home of champions",
                    "default_action": {
                        "type": "postback",
                        "webview_height_ratio": "COMPACT",
                    },
                    "buttons":[
                    {
                        "type": "postback",
                        "title":"NCU",
                        "payload":"ncu"
                    }              
                    ]      
                }
                ]
            }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)

    if r.status_code != 200:
        print(r.status_code)
        print(r.text)



def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)