# Driver program for testing REST API for login

# USAGE
# python login_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/login'
headers = {'Content-Type' : 'application/json'}

login_data = {'mobile_no': 8378409943, 'password': 'encrypted_pw'}


# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(login_data), headers = headers).json()

# ensure the request was sucessful
if r['success']:
	print ('Login Request succeeded')
	print r
	
# otherwise, the request failed
else:
	print ('Login Request failed')
	print r
