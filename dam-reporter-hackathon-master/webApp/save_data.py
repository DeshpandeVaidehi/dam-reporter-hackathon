# Driver program for testing REST API for saving data of dam in distress condition

# USAGE
# python save_data.py

# import the necessary packages
import requests
import json

# initialize the REST API endpoint URL
URL_FOR_ORDER = 'http://localhost:5000/save_data'
headers = {'Content-Type' : 'application/json'}

dam_data = {'aadhaar_no': 945555421345, 'dam_name': 'Paithan (Jayakwadi)', 'descrip': 'The dam has now become weaker', 'seepage': '0', 'cracks':'1', 'erosion':'0', 'gates_condition':'1', 'sluice_gates_condition':'1', 'max_flood_handled':250, 'energy_dissipator_condition':'1', 'instrument_condition':'1', 'latitude': 65.6, 'longitude': 45.78, 'image1': 'null', 'image2': 'null2'}


# submit the request
r = requests.post(URL_FOR_ORDER, data = json.dumps(dam_data), headers = headers).json()

# ensure the request was sucessful
if r['success']:
	print ('Request succeeded')
	
# otherwise, the request failed
else:
	print ('Request failed')
