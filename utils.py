from wit import Wit 

access_token = "UDKKZG7KB6Q4G7S24E325L6QFKFPJRWG"

client = Wit(access_token = access_token)

def wit_response(message):
    response = client.message(message)
    entity = None
    value = None

    try:
        entity = list(response['entities'])[0]
        value = response['entities'][entity][0]['value']
    except:    
        pass 
    return (entity, value)


print(wit_response("Show me some Scholarships")) 