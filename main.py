from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import time

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
personal_phone_number = 'your_personal_phone_number'
client = Client(account_sid, auth_token)

url = 'the url of the website you want to monitor'
element = 'the component path of the specific element you want to monitor'

def get_element_content():
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    element_selector = soup.select_one(element)
    return element_selector.get_text()

def send_sms(mess):
    message = client.messages.create(
        body=mess,
        from_=twilio_phone_number,
        to=personal_phone_number
    )
    print(message.sid)

def monitor_element_change():
    previous_content = get_element_content()
    while True:
        try:
            current_content = get_element_content()
            print(previous_content)

            if current_content != previous_content and len(current_content) == 0:
                change_message = "There is an empty seat in CS330, get it quick!" #customize message
                send_sms(change_message)
                print(change_message)

            previous_content = current_content
            time.sleep(30)  #adjust for how often you want to check

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(300)  #wait for 5 minutes before retrying in case of an error

if __name__ == "__main__":
    monitor_element_change()