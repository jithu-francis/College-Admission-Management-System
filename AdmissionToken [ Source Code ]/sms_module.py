import csv
import sms



def create_token_dictionary(csv_filename):
    token_data = {}

    try:
        with open(csv_filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                token = int(row['Token'])
                name = row['Name']
                phone = row['Phone']
                token_data[token] = {'name': name, 'phone': phone}
    except FileNotFoundError:
        # Handle file not found case
        pass

    return token_data

# Call the function to create the dictionary from the CSV file

# print(token_data)
# Now you can use the token_data dictionary as before
# for token, data in token_data.items():
#     print(f"Token: {token}")
#     print(f"Name: {data['name']}")
#     print(f"Phone Number: {data['phone']}")
#     print("-" * 30)

def send_message(token_number):
    token_data = create_token_dictionary('token_data.csv')
    
    item = token_data[token_number]
    phone = item['phone']
    print(phone)

    

    # print(token_number)
    if token_number in token_data:
        current_person = token_data[token_number]
        next_token = token_number + 1

        if next_token in token_data:
            next_person = token_data[next_token]

            message_current = f"Token number {token_number}, {current_person['name']}, Please come to the counter."
            #sms.send_sms(message_current, phone) #Uncomment these to send sms

            message_next = f"Token number {next_token}, {next_person['name']}, Please be ready, you are next."

            item2 = token_data[next_token]
            phone2 = item2['phone']

            #sms.send_sms(message_next, phone2)  #Uncomment these to send sms

            print(message_current)
            print(message_next)
        else:
            print(f"Token Number {token_number}, Please come to the counter!")
            #sms.send_sms(message_current, phone) #Uncomment these to send sms
            print("No next person found.")
    else:
        print("Token number not found.")

# send_message(1)

def send_message_wait(token_number):
    token_data = create_token_dictionary('token_data.csv')
    if token_number in token_data:
        current_person = token_data[token_number]
        message_current = f"Token number {token_number}, {current_person['name']}, you need to come to the counter."
        print(message_current)

"""def send_message_generated(token_number):
    token_data = create_token_dictionary('token_data.csv')
    if token_number in token_data:
        current_person = token_data[token_number]
        message_current = f"Your Token Number is: {token_number}, {current_person['name']}."
        print(message_current)"""