from twilio.rest import Client
import requests




def send_sms(message, recipient):
    account_sid = 'AC92c272072cced50fffd18799fb511dae'
    auth_token = 'dba758b82377dec4fe1b7dbc4fb17a69'

    client = Client(account_sid, auth_token)

    #message to be sent
    message_text = message

    #reciever s phone number
    recipient_number = recipient

    message = client.messages.create(
        body = message_text,
        from_= '+12296963923',
        to = recipient_number
    )

    #affirmation
    print('sms sent')



"""def send_sms(message, recipient):
    # Replace 'YOUR API KEY HERE' with your actual Fast2SMS API key
    api_key = 'tP7sbhRGEzgivrdeAZuHyMwUSxJW2mI0cLnkFa6qCYfKQTXjNlWeNdL5hp7BnSYrTJQwZ1sR92AvMgcm'


    # Create a dictionary for the SMS data
    sms_data = {
        'sender_id': 'FSTSMS',  # Your default Sender ID
        'message': message,  # Put your message here!
        'language': 'english',
        'route': 'p',
        'numbers': response  # You can send SMS to multiple numbers
    }
    headers = {
        'authorization': api_key,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    # Send the SMS using the Fast2SMS API
    response = requests.post(url, data=sms_data, headers=headers)


    
    # Print the response
    print(response.text)  """ 
