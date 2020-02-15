# Driver program for testing REST API for signup

# USAGE
# python signup_request.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/signup'
headers = {'Content-Type' : 'application/json'}

signup_data = {'aadhaar_no': 945555421345, 'name': 'Pinal Shah', 'password': 'encrypted_pw', 'mobile_no': 8378409943, 'email_id': 'shahpinal@gmail.com', 'authority_level': '0'}

# authority_level = '0' (for common users), '1' (for auditors), '2' (for ministries governing water bodies), '3' (for states governing water bodies)

# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(signup_data), headers = headers).json()

# ensure the request was sucessful
if r['success']:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ('Request failed')
	print r['remark']
