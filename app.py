import os, sys
import json
from flask import Flask, request
import requests
from pymessenger import Bot
from student import Student

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAhLsI2qzIsBAPERskZCI0XIZBk71SLX3uT1huOBU8f3RnsTsBIm5xPmgAGlPjLZBV9hqV3zQUk3abhgsabE1LiIPuv0uZCCo1ZBRpe2AwuZAXgJMiWOddrO3GAg8rrztNLhZBYyna6FNJCDDMJ4ZCt1uOLRmuTNIzrMpAvZANBFNZAOtTV52TFFJW"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "Sl33pyW00ly"

GREETINGS = ['Is anyone available to chat?','Hi, i need some help' ,'Hey', 'hey', 'Hi', 'hi', 'hello', 'Hello', 'good afternoon', 'i have a question']
FAREWELL = ['goodbye', 'bye', "Thanks for the info", 'Bless', 'thank you', 'Thank you']

buttons = [
    {
        'response': ['Yes', 'No'],
        'payload': '0'
    },    
    {
        'YEARS':["1st Year", "2nd Year", "3rd Year", "Final Year"],
        'payload': '1'
    },
    {
        'MAJORS':["Computer Science", "Social Sciences", "Medicine", "Any"],
        'payload': '2'
    },
    {
        'response': ["Yes, please continue", "No, I'm good"],
        'payload': '7'
    }
]

UWI = [
    [ #SOCIAL SCIENCES
        {
            'title': "AFUWI SCHOLARSHIPS",
            'subtitle': "Value: US$ 2,000-5000, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/afuwi-scholarships-0#overlay=node/914/edit&overlay-context=scholarships-bursaries"
        },
        {
            'title': "AMBASSADOR J. GARY COOPER BURSARY",
            'subtitle': "Value: J$120,000.00, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/ambassador-j-gary-cooper-bursary-0#overlay-context=scholarships-bursaries"
        },
        {
            'title': "OFFICE OF STUDENT FINANCING SCHOLARSHIP",
            'subtitle': "Value: J$150,000.00, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/office-student-financing-scholarship-0#overlay-context=scholarships-bursaries"
        }
    ],
    [ #COMPUTER SCIENCE
        {
            'title': "NCB Software Engineering Scholarship",
            'subtitle': "Value: US $5,000.00, Four (4) years",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/ncb-software-engineering-scholarship"
        },
        {
            'title': "DIGICEL SCHOLARSHIPS",
            'subtitle': "Value: J$145,000.00, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/digicel-scholarships-0"
        },
        {
            'title': "JOE PEREIRA SCHOLARSHIP (THE)",
            'subtitle': "Value: J $250,000.00, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/joe-pereira-scholarship-1#overlay-context=scholarships-bursaries"
        }
    ],
    [ #MEDICINE
        {
            'title': "Dr. Denise Mitchell- Thwaites Scholarship",
            'subtitle': "J $ 2 million per year, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/dr-denise-mitchell-thwaites-scholarship-0"
        },
        {
            'title': "IGL RAZAI AZARD RAHAMAN SCHOLARSHIP FOR MEDICINE",
            'subtitle': "Value: J$120,000.00, One (1) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/igl-razai-azard-rahaman-scholarship-medicine-0#overlay-context=scholarships-bursaries"
        },
        {
            'title': "OFFICE OF STUDENT FINANCING SCHOLARSHIP",
            'subtitle': "Value: J$650,000.00, Fine (5) year",
            'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/office-student-financing-scholarship-0#overlay-context=scholarships-bursaries"
        }
    ]
]

Utech = [
    [
        {
            "title": "Carreras Seek",
            "subtitle": "3.0 GPA"
        },
        {
            "title": "Jamaica Bauxite Mining Limited (Glencore)",
            "subtitle": "Resides in a bauxite parishes"
        },
        {
            "title": "Joan Duncan Trust",
            "subtitle": "Joan Duncan School of Entrepreneurship, Ethics & Leadership"       
        }
    ],
    [
        {
            "title": "Grace Kennedy Foundation (Douglas Orane)",
            "subtitle": "Faculty of Engineering & Computing"
        },
        {
            "title": "Gregory Vassell Memorial",
            "subtitle": "Atleast 3.0 GPA"
        },
        {
            "title": "Students’ Union Faculty of Engineering & Computing",
            "subtitle": "at least a B- average"
        }
    ],
    [
        {
            "title": "Mona (Hurd) Style",
            "subtitle": "Pharmaceutical Technology"
        },
        {
            "title": "Carol A. Lewis (Ivy M. Ellis)",
            "subtitle": "Health Records & Statistics. College of Health Sciences"
        },
        {
            "title": "UTech Foundation (Mable Tenn)",
            "subtitle": "3rd year Pharmacy, College of Health Sciences"       
        }
    ]
]

Any = [
    {
        'title': "Bernie & Ramona Benson",
        'subtitle': "1st year of All Schools"
    },
    {
        'title': "Chinese Ambassador",
        'subtitle': "all Schools"
    },
    {
        'title': "Guild Part Time Assistance (P.T.A) Grant",
        'subtitle': "Value: J $150,000.00, One (1) year",
        'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/guild-part-time-assistance-pta-grant" 
    },
    {
        'title': "Advent Fellowship Scholarship",
        'subtitle': "Value: JMD $100,000, One (1) year",
        'buttonUrl': "https://www.mona.uwi.edu/osf/scholarships/advent-fellowship-scholarship"
    }
]

imgUrl = [
    {
        'imageUrl': "https://www.utech.edu.jm/about-utech/utech.jpg"
    },
    {
        'imageUrl':"https://sta.uwi.edu/newspics/2020/Regional%20crest%20INtranet.jpg"
    }
]


student = Student("No", "Any", "Any", "Any")


@app.route('/', methods=['GET'])
def verify():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    getstarted()
    return "WEBHOOK VERIFIED", 200
    
def getstarted():
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
            }
    })

    r = requests.post('https://graph.facebook.com/v7.0/me/messenger_profile?access_token='+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
    greetingText()

def greetingText():
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "greeting": [{
            "locale":"default",
            "text":"Let' get this bag ! I mean scholarships." 
            }
        ]
    })

    try:
        r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
        print (r.text)
        r.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

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

        #Handles messages events
        if messaging_event.get('message'):
            handleMessage(sender_psid, messaging_event['message'])
                    
        elif messaging_event.get('postback'):
            handlePostback(sender_psid, messaging_event['postback'])

        return "ok", 200
    else:
        #Return a '404 Not Found' if event is not from a page subscription
        return "error", 404

#handles message reply
def handleMessage(sender_psid, received_message):
    response = {}

    if ('quick_reply' in received_message.keys()):
        payload = received_message['quick_reply']['payload']
        response_message = received_message['text']
        if (payload == buttons[1]['payload']):
            student.years = received_message
            response = {
                "text": "That's great. We have a few listings here.."
            }
            callSendAPI(sender_psid, response)
            response = {
                "attachment": {
                    "type":"template",
                    "payload": {
                        "template_type":"generic",
                        "elements":[
                            {
                                "title":"University of Technology",
                                "image_url":"https://www.utech.edu.jm/about-utech/utech.jpg",
                                "subtitle":"Utech",
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.utech.edu.jm/admissions/dsf/financial-aid/scholarships/scholarships-listing",
                                        "title":"Full Listing",
                                        "webview_height_ratio": "full",
                                        "messenger_extensions": "true",  
                                        "fallback_url": "https://www.utech.edu.jm/admissions/dsf/financial-aid/scholarships/scholarships-listing"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Scholarship Form",
                                        "payload":"3"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Continue",
                                        "payload":"4"
                                    }              
                                ]      
                            },
                            {
                                "title":"University of the West Indies",
                                "image_url":"https://sta.uwi.edu/newspics/2020/Regional%20crest%20INtranet.jpg",
                                "subtitle":"UWI",
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.mona.uwi.edu/osf/scholarships-bursaries",
                                        "title":"Full Listing",
                                        "webview_height_ratio": "full",
                                        "messenger_extensions": "true",  
                                        "fallback_url": "https://www.mona.uwi.edu/osf/scholarships-bursaries"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Scholarship Form",
                                        "payload":"5"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Continue",
                                        "payload":"6"
                                    }              
                                ]      
                            }
                        ]
                    }
                }
            }

        elif (payload == buttons[0]['payload']):
            student.specialNeeds = received_message['text']
            response = {
                "text": "Let's get this show on the road!"
            }
            callSendAPI(sender_psid, response)
            response = "What year are you in ?" 
            response = postback_button_response(response, buttons[1]['payload'], buttons[1]['YEARS'])

        elif(payload == buttons[2]['payload']):
            student.major = response_message
            response = {
                "text": "Getting your results.. Give me a sec."
            }
            callSendAPI(sender_psid, response)
            getResults(sender_psid)
            response = {
                "text": "This is all we have for you right now. Please feel free to restart the conversation at any time."
            }
            callSendAPI(sender_psid, response)
            response = {
                "text": "Scholly out."
            }

        elif(payload == buttons[3]['payload']):
            if ('Yes' in response_message):
                response = getMajor(sender_psid)
            elif('No' in response_message):
                response = "Sorry to see you leave us so soon, but thanks for your time. Hope your with us again." 
                response = {
                    "text": response
                }
                callSendAPI(sender_psid, response)
                response = {
                    "text": "Scholly out."
                }

        callSendAPI(sender_psid, response)
        return

    elif 'text' in received_message.keys():
        messaging_text = received_message['text']
        if messaging_text in GREETINGS:
            try:
                firstName = retrieve_user_information(sender_psid)['first_name']
            except:
                firstName = ''
            response = "Hey " + firstName + ", I'm Scholly your assistant bot for today."
            response = {
                "text": response
            }
            callSendAPI(sender_psid, response)
            response = "Welcome to Scholarly, where scholarships islandwide are placed in an easy to access way for all university students." 
            response = {
                "text": response
            }
            callSendAPI(sender_psid, response)
            response = {
                "text": "First we will need to know a little about you."
            }
            callSendAPI(sender_psid, response)
            response = "Are you a special needs student ?"
            response = postback_button_response(response, buttons[0]['payload'], buttons[0]['response'])
            callSendAPI(sender_psid, response)

def postback_button_response(text, payload, titles):
    quick_replies = []
    for title in titles:
        quick_replies.append({
            'content_type': 'text',
            'title': title,
            'payload' : payload,
        })

    return {
        'text': text,
        'quick_replies': quick_replies
    }

def typingSenderAction(sender_psid):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(
        {"recipient": {
            "id": sender_psid
            },
            "sender_action":"typing_on"
        })

    try:
        r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
        print (r.text)
        r.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

# Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(
        {"recipient": {
            "id": sender_psid
            },
            "message": response,
            "sender_action": None
        })

    try:
        typingSenderAction(sender_psid)
        r = requests.post("https://graph.facebook.com/v7.0/me/messages?access_token="+ PAGE_ACCESS_TOKEN, headers=headers, data=data)
        print (r.text)
        # If the response was successful, no Exception will be raised
        r.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

def handlePostback(sender_psid, received_postback):
    #if("postback" in received_postback):
    payload = received_postback["payload"]
    if (payload == '3'):
        student.school = "Utech"
        response = {
            "text": "https://www.surveymonkey.com/r/UTECHScholarshipApplication"
        }
        callSendAPI(sender_psid, response)

    elif (payload == '5'):
        student.school = "UWI"
        response = {
            "text": "https://www.mona.uwi.edu/osf/sites/default/files/osf/scholarship_bursary_application_form_2020_2021.pdf"
        }
        #print(student.school)
        callSendAPI(sender_psid, response)

    
    if(payload == '3' or payload == '5'):
        response = "Do you want continue ?"
        response = postback_button_response(response, buttons[3]['payload'], buttons[3]['response'])
        callSendAPI(sender_psid, response)
    
    elif(payload == '4' or payload == '6'):
        if(payload == '4'):
            student.school = "Utech"
        elif(payload == '6'):
            student.school = "UWI"

        response = getMajor(sender_psid)
        callSendAPI(sender_psid, response)

def getMajor(sender_psid):
    response = {
        "text": "Great I just need one more piece of info."
    }
    callSendAPI(sender_psid, response)
    response = "What is your current major ?"
    response = postback_button_response(response, buttons[2]['payload'], buttons[2]['MAJORS'])
    return response

def getResults(sender_psid):
    response = {}
    elements = []
    
    print(student.school)
    print(student.major)

    if("UWI" in student.school):
        title = "View"
        if("Social Sciences" in student.major):
            schList = UWI[0]

        if("Computer Science" in student.major):
            schList = UWI[1]
        
        if("Medicine" in student.major):
            schList = UWI[2]
            
    elif("Utech" in student.school):
        title = "See Application"
        if("Social Sciences" in student.major):
            schList = Utech[0]

        if("Computer Science" in student.major):
            schList = Utech[1]
        
        if("Medicine" in student.major):
            schList = Utech[2]        

    if("Any" in student.major):
        schList = Any


    for sch in schList:
        if('buttonUrl' in sch.keys()): #if UWI
            url = sch['buttonUrl']
            img = imgUrl[1]['imageUrl']
            title = "View"
        else: #if UTECH
            url = "https://www.surveymonkey.com/r/UTECHScholarshipApplication"
            img = imgUrl[0]['imageUrl']
            title = "Application Form"

        elements.append({
            "title":sch['title'],
            "image_url": img,
            "subtitle":sch['subtitle'],
            "buttons":[
                {
                    "type":"web_url",
                    "url": url,
                    "title":title,
                    "webview_height_ratio": "full",
                    "messenger_extensions": "true",  
                    "fallback_url": url
                }              
            ]  
        })

    response = {
        "attachment": {
            "type":"template",
            "payload": {
                "template_type":"generic",
                "elements": elements
            }
        }
    }

    callSendAPI(sender_psid, response)            

def retrieve_user_information(sender_psid):
    try:
        # Send the HTTP request to the Messenger Platform
        response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_psid, PAGE_ACCESS_TOKEN))

        # If the response was successful, no Exception will be raised
        #response.raise_for_status()

        return json.loads(response.content)
    except requests.HTTPError as http_err:
        pass
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True, port = 80)