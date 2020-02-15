# Driver program for testing REST API for getting report

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/get_report'
headers = {'Content-Type' : 'application/json'}

report_data = {'start_date': '2018-03-21', 'end_date': '2018-04-02', 'criteria': 1}

# criteria = 1 (for report generation according to state), 2 (for report generation according to priority), 3 (for report generation according to facility)

# submit the request
report = requests.post(URL_FOR_ORDER, data = json.dumps(report_data), headers = headers).json()

# ensure the request was sucessful
if report['success']:
	print ('Request succeeded')
	print report
	
# otherwise, the request failed
else:
	print ('Request failed')
	print report
