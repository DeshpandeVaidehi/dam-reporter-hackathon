# Driver program for testing REST API for getting entry details

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ENRTY = 'http://localhost:5000/get_entry_details'
headers = {'Content-Type' : 'application/json'}

report_data = {'time_stamp': '2018-03-21', 'dam_name': 'Paithan (Jayakwadi)', 'aadhaar_no': 945555421345}


# submit the request
report = requests.post(URL_FOR_ENTRY, data = json.dumps(report_data), headers = headers).json()

# ensure the request was sucessful
if report['success']:
	print ('Request succeeded')
	print report
	
# otherwise, the request failed
else:
	print ('Request failed')
	print report
