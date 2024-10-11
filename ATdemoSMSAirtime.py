from flask import Flask, request, make_response
import africastalking
from xml.etree.ElementTree import Element, SubElement, tostring

app = Flask(__name__)

# Initialize Africa's Talking
africastalking.initialize(
    username='YOUR_USERNAME',
    api_key='YOUR_API_KEY'
)
voice = africastalking.Voice
sms = africastalking.SMS
airtime = africastalking.Airtime

# Survey questions
questions = [
    "Rate your overall experience at PyCon 2024 from 1 to 5, where 1 is poor and 5 is excellent.",
    "Rate the quality of presentations and workshops from 1 to 5, where 1 is low and 5 is high.",
    "Rate the likelihood of attending PyCon next year from 1 to 5, where 1 is unlikely and 5 is very likely."
]

@app.route('/voice', methods=['POST'])
def handle_call():
    session_id = request.values.get("sessionId", None)
    is_active = request.values.get("isActive", False)

    if is_active == "1":
        return start_survey()
    else:
        return end_call()

def start_survey():
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/question1">'
    response += '<Say>Welcome to the PyCon 2024 survey. Please rate your overall experience on a scale of 1 to 5, where 1 is poor and 5 is excellent. Press the hash key when done.</Say>'
    response += '</GetDigits>'
    response += '</Response>'
    return response

@app.route('/question1', methods=['POST'])
def handle_question1():
    digits = request.values.get("dtmfDigits", None)

    if digits and digits in "12345":
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/question2">'
        response += '<Say>Thank you. Now, please rate the quality of presentations and workshops on a scale of 1 to 5, where 1 is low and 5 is high. Press the hash key when done.</Say>'
        response += '</GetDigits>'
        response += '</Response>'
    else:
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>Invalid input. Please try again.</Say>'
        response += '<Redirect>https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/voice</Redirect>'
        response += '</Response>'

    return response

@app.route('/question2', methods=['POST'])
def handle_question2():
    digits = request.values.get("dtmfDigits", None)

    if digits and digits in "12345":
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/question3">'
        response += '<Say>Thank you. Finally, how likely are you to attend PyCon again next year? Please rate on a scale of 1 to 5, where 1 is unlikely and 5 is very likely. Press the hash key when done.</Say>'
        response += '</GetDigits>'
        response += '</Response>'
    else:
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>Invalid input. Please try again.</Say>'
        response += '<Redirect>https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/question1</Redirect>'
        response += '</Response>'

    return response

@app.route('/question3', methods=['POST'])
def handle_question3():
    digits = request.values.get("dtmfDigits", None)
    caller_number = request.values.get("callerNumber", None)

    if digits and digits in "12345":
        # Send SMS
        try:
            sms_response = sms.send("Thank you for completing the PyCon 2024 survey!", [caller_number])
            print(f"SMS sent successfully: {sms_response}")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")

        # Send Airtime
        try:
            airtime_response = airtime.send(recipients=[
                {"phoneNumber": caller_number, "amount": 500, "currency_code": "UGX"}
            ])
            print(f"Airtime sent successfully: {airtime_response}")
        except Exception as e:
            print(f"Error sending airtime: {str(e)}")

        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>Thank you for completing our survey. Your feedback is valuable to us. You will receive an SMS confirmation and airtime reward shortly. Goodbye!</Say>'
        response += '</Response>'
    else:
        response = '<?xml version="1.0" encoding="UTF-8"?>'
        response += '<Response>'
        response += '<Say>Invalid input. Please try again.</Say>'
        response += '<Redirect>https://9d342628-dd04-471d-8b7b-8ad03318c81a-00-35ds236hld8r4.worf.replit.dev/voice/question2</Redirect>'
        response += '</Response>'

    return response

def end_call():
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    response += '<Say>Thank you for your time. Goodbye!</Say>'
    response += '</Response>'
    return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
