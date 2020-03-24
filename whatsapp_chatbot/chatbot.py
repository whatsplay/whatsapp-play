
import os    
from twilio.rest import Client

credential_path = os.environ.get('credential_path')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


import dialogflow
from google.api_core.exceptions import InvalidArgument
DIALOGFLOW_PROJECT_ID = 'mypizzabot-elkbil'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS =os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
SESSION_ID = os.environ.get('SESSION_ID')

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
client = Client(account_sid, auth_token)

from_whatsapp_number='whatsapp:+14155238886'
to_whatsapp_number=os.environ.get('to_whatsapp_number')
text_to_be_analyzed =" "
while text_to_be_analyzed!="Thanks" :
    text_to_be_analyzed = input()
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    
    client.messages.create(
         body=response.query_result.query_text,  
         from_=from_whatsapp_number,
         to=to_whatsapp_number)
    
    client.messages.create(
         body=response.query_result.fulfillment_text,  
         from_=from_whatsapp_number,
         to=to_whatsapp_number)
    

