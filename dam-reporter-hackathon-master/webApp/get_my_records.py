# Driver program for testing REST API for getting report

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_RECORDS = 'http://localhost:5000/get_my_records'
headers = {'Content-Type' : 'application/json'}

report_data = {'aadhaar_no': 945555421345, 'start_date': '2018-03-31', 'end_date': '2018-04-02'}


# submit the request
report = requests.post(URL_FOR_RECORDS, data = json.dumps(report_data), headers = headers).json()

# ensure the request was sucessful
if report['success']:
	print ('Request succeeded')
	print report
	
# otherwise, the request failed
else:
	print ('Request failed')
	print report
