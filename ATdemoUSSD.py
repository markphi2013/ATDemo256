import africastalking
from flask import Flask, make_response, request

# Initialize Africa's Talking
username = "YOUR_USERNAME"
api_key = "YOUR_API_KEY"
africastalking.initialize(username, api_key)

# Initialize USSD and Voice services
ussd = africastalking.USSD
voice = africastalking.Voice

app = Flask(__name__)

def make_call(phone_number):
    try:
        # Make a call
        call_from = "+256323200793"  # Replace with a valid Africa's Talking voice number
        result = voice.call(call_from, [phone_number])
        print(f"Call initiated: {result}")
    except Exception as e:
        print(f"Error making call: {str(e)}")

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    response = ""

    if text == "":
        # This is the first request. Note how we start the response with CON
        response = "CON Welcome to Pycon 2024! Do you consent to receive a phone call?\n"
        response += "1. Yes\n"
        response += "2. No"
    elif text == "1":
        # User selected Yes
        make_call(phone_number)  # Initiate the call
        response = "END Thank you! You will receive a phone call shortly."
    elif text == "2":
        # User selected No
        response = "END Thanks for your interest in our services."
    else:
        response = "END Invalid input. Please try again."

    # Send the response back to the API
    return make_response(response, 200, {'Content-Type': 'text/plain'})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
