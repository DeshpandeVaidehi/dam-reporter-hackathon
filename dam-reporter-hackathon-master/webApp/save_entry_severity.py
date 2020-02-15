import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/save_entry_severity'
headers = {'Content-Type' : 'application/json'}

data = {'time_stamp': '2018-03-31 05:34:22', 'dam_name': 'Paithan (Jayakwadi)', 'aadhaar_no': 945555421345, 'severity': '1'}

# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(data), headers = headers).json()

# ensure the request was sucessful
if r['success']:
	print ('Request succeeded')
	print r
	
# otherwise, the request failed
else:
	print ('Request failed')
	print r
