# Driver program for 1testing REST API for getting notifications

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/get_notifications'
headers = {'Content-Type' : 'application/json'}

user_data = {'aadhaar_no': 945555421345}

# submit the request
notif = requests.post(URL_FOR_ORDER, data = json.dumps(user_data), headers = headers).json()

# ensure the request was sucessful
if notif['success']:
	print ('Request succeeded')
	print notif

# otherwise, the request failed
else:
	print ('Request failed')
	print notif
