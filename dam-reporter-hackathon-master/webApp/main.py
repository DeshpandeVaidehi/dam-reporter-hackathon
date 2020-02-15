from flask import Flask, render_template, redirect, url_for
import json
import subprocess
from flask import request
import flask
from flask_cors import CORS, cross_origin

import mysql.connector

import time
import datetime

import urllib2
import cookielib
import sys
import os
from stat import *

app = Flask(__name__)
CORS(app)

username = 'Yogiraj'
dbpassword = '123456'
host = '127.0.0.1'
database_name = 'hackathon'


@app.route("/login_ui", methods=["POST", "GET"])
def login_ui():
	return render_template('login.html')

@app.route("/signup_ui", methods=["POST", "GET"])
def signup_ui():
	return render_template('signup.html')

@app.route("/signup_ui_audit", methods=["POST", "GET"])
def signup_ui_audit():
	return render_template('signup_audit.html')

@app.route("/signup_ui_minist", methods=["POST", "GET"])
def signup_ui_minist():
	return render_template('signup_minist.html')

@app.route("/")
def index():
	return render_template("index.html", msg="welcome")


@app.route('/index', methods=['GET', 'POST'])
def home():
	return render_template("index.html", msg="welcome")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		#print request.data
		if request.is_json:
			signup_content = request.get_json()
			print signup_content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for signup (DB Insertion) :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor()

			signup_query = ("INSERT INTO login " "(aadhaar_no, name, mobile_no, email, passwd, authority_level, city) " "VALUES (%(aadhaar_no)s, %(name)s, %(mobile_no)s, %(email_id)s, %(password)s, %(authority_level)s, %(city)s)")

			try:
				cursor.execute(signup_query, signup_content)

				# Make sure data is committed to the database
				cnx.commit()

				# indicate that the request was a success
				ack["success"] = True

		 	except Exception as e:
		 		print e
		 		ack['remark'] = 'Aadhaar number already exists'

			cursor.close()
			cnx.close()

			# return the data dictionary as a JSON response
			return flask.jsonify(ack)

		else:
			print "Not json"


	else:
		print "Not a POST request"
	#return render_template("index.html", msg="welcome")


# Following endpoint can be called by client on 'http://localhost:5000/login' url.

@app.route("/login", methods=['GET', 'POST'])
def login():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		#print request.data
		if request.is_json:
			login_content = request.get_json()
			print login_content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for login (DB checking) :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)

			login_query = ("SELECT aadhaar_no, name, email, authority_level, notification_id FROM login WHERE mobile_no = %(mobile_no)s AND passwd = %(password)s")

			try:
				cursor.execute(login_query, login_content)
				rows_affected = cursor.rowcount

				if rows_affected == 1:
					# Send user details :-
					#rows = cursor.fetch_all()
					#row = rows[0]

					for (aadhaar_no, name, email, authority_level, notification_id) in cursor:
						ack['aadhaar_no'] = aadhaar_no
						ack['name'] = name
						ack['email'] = email
						ack['authority_level'] = authority_level
						ack['notification_id'] = notification_id
						ack['password'] = login_content['password']

					'''ack['aadhaar_no'] = row[0]
					ack['name'] = row[1]
					ack['email'] = row[2]
					ack['authority_level'] = row[3]
					ack['notification_id'] = row[4]'''

					# indicate that the request was a success
					ack["success"] = True

				else:
					# indicate that the login request failed
					ack["success"] = False
					ack["remark"] = "User not recognized"

		 	except Exception as e:
		 		print 'here', e, 'here'

			cursor.close()
			cnx.close()

			print ack

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		mobile_no = request.args.get('mob_no');
		password = request.args.get('passw');
		cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
		cursor = cnx.cursor(buffered = True)
		
		login_query = ("SELECT aadhaar_no, name, email, authority_level, notification_id FROM login WHERE mobile_no = %s AND passwd = %s")
		
		try:
			cursor.execute(login_query, (mobile_no, password))
			rows_affected = cursor.rowcount
	
			if rows_affected == 1:

				for (aadhaar_no, name, email, authority_level, notification_id) in cursor:

					#session['aadhaar'] = aadhaar_no
					print authority_level, email
					context = {'user': name, 'aadhaar': aadhaar_no}
					if(authority_level == '0'):
						return render_template('sih_common.html', **context);
					if(authority_level == '1'):
						return render_template('siht_auditor.html', **context);
					if(authority_level == '2'):
						return render_template('sihm_ministry.html', **context);
			else:
				return render_template('login.html');
		except:
				return render_template('login.html');
	#return render_template("index.html", msg="welcome")


@app.route("/save_data", methods=['GET', 'POST'])
def save_data():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		#print request.data, type(request.data)
		if request.is_json:
			dam_content = request.get_json()
			#print dam_content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']
			
			#print dam_content['image1'], dam_content['image2']

			# Code for saving data of dam in distress condition (DB Insertion) :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)

			cursor = cnx.cursor(buffered=True)

			dam_query = ("SELECT dam_id FROM dam WHERE dam_name = %(dam_name)s")

			try:
				cursor.execute(dam_query, dam_content)
				rows_affected = cursor.rowcount

				if rows_affected == 1:
					damid = 0
					for (dam_id, ) in cursor:
						damid = dam_id
						print "dam_id = ", damid

					ts = time.time()
					data_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

					# Insert into dam_data table

					#dam_query = ("INSERT INTO dam_data " "(seepage, cracks, latitude, longitude, time_stamp, aadhaar_no, dam_id, descrip) " "VALUES (%(seepage)s, %(cracks)s, %(latitude)s, %(longitude)s, " + data_timestamp + ", %(aadhaar_no)s, " + str(damid) + " , %(descrip))")
					# dam_data = {'aadhaar_no': 945555421345, 'dam_name': 'Paithan (Jayakwadi)', 'descrip': 'The dam has now become weaker', 'seepage': '0', 'cracks':'1', 'erosion':'0', 'gates_condition':'1', 'sluice_gates_condition':'1', 'max_flood_handled':250, 'energy_dissipator_condition':'1', 'latitude': 65.6, 'longitude': 45.78}

					#if dam_content['image2'] != "null" and dam_content['image1'] != 'null':
					#	print '1'
					dam_query = ("INSERT INTO dam_data " "(seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, aadhaar_no, dam_id, descrip, image1, image2) " "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

					cursor.execute(dam_query, (dam_content['seepage'], dam_content['cracks'], dam_content['erosion'], dam_content['gates_condition'], dam_content['sluice_gates_condition'], dam_content['max_flood_handled'], dam_content['energy_dissipator_condition'], dam_content['instrument_condition'], dam_content['latitude'], dam_content['longitude'], data_timestamp, dam_content['aadhaar_no'], str(damid), dam_content['descrip'], dam_content['image1'], dam_content['image2']))

					
					#elif dam_content['image2'] == "null" and dam_content['image1'] != "null":
					#	print '2'
					#	dam_query = ("INSERT INTO dam_data " "(seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, aadhaar_no, dam_id, descrip, image1) " "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

					#	cursor.execute(dam_query, (dam_content['seepage'], dam_content['cracks'], dam_content['erosion'], dam_content['gates_condition'], dam_content['sluice_gates_condition'], dam_content['max_flood_handled'], dam_content['energy_dissipator_condition'], dam_content['instrument_condition'], dam_content['latitude'], dam_content['longitude'], data_timestamp, dam_content['aadhaar_no'], str(damid), dam_content['descrip'], dam_content['image1']))

					
					#else:
					#	print '3'
					#	dam_query = ("INSERT INTO dam_data " "(seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, aadhaar_no, dam_id, descrip) " "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

					#	cursor.execute(dam_query, (dam_content['seepage'], dam_content['cracks'], dam_content['erosion'], dam_content['gates_condition'], dam_content['sluice_gates_condition'], dam_content['max_flood_handled'], dam_content['energy_dissipator_condition'], dam_content['instrument_condition'], dam_content['latitude'], dam_content['longitude'], data_timestamp, dam_content['aadhaar_no'], str(damid), dam_content['descrip']))
						
					
					# Make sure data is committed to the database
					cnx.commit()

					# indicate that the request was a success
					ack["success"] = True

				else:
					ack["success"] = False
					ack["remark"] = "Dam name wrong"

		 	except Exception as e:
		 		print e

			cursor.close()
			cnx.close()

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"

	#return render_template("index.html", msg="welcome")


@app.route("/get_notifications", methods=['GET', 'POST'])
def get_notifications():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		#print request.data
		if request.is_json:
			content = request.get_json()
			print content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for getting notifications :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)
			print content['aadhaar_no']

			#query = ("select seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, descrip from dam_data join login on  dam_data.aadhaar_no = "+ content['aadhaar'] +" where login.notification_id > dam_data.dam_data_id")
			query = ("select dam_name, nearest_city, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, descrip from dam_data join dam on dam_data.dam_id = dam.dam_id where dam_data_id > (select notification_id from login where aadhaar_no = %(aadhaar_no)s )")

			try:
				cursor.execute(query, content)
				rows_affected = cursor.rowcount

				print rows_affected

				if rows_affected > 0:
					ack['report'] = []

					for (dam_name, nearest_city, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, latitude, longitude, time_stamp, descrip) in cursor:
						repo = {}
						repo['dam_name'] = dam_name
						repo['nearest_city'] = nearest_city
						repo['seepage'] = seepage
						repo['cracks'] = cracks
						repo['erosion'] = erosion
						repo['gates_condition'] = gates_condition
						repo['sluice_gates_condition'] = sluice_gates_condition
						repo['max_flood_handled'] = max_flood_handled
						repo['energy_dissipator_condition'] = energy_dissipator_condition
						repo['instrument_condition'] = instrument_condition
						repo['latitude'] = latitude
						repo['longitude'] = longitude
						repo['time_stamp'] = time_stamp
						repo['descrip'] = descrip
						print repo

						ack['report'].append(repo)

					updateQuery = ("UPDATE login SET notification_id = (SELECT max(dam_data_id) from dam_data) where aadhaar_no = %(aadhaar_no)s")
					cursor.execute(updateQuery, content)

					# Make sure data is committed to the database
					cnx.commit()

					# indicate that the request was a success
					ack["success"] = True

				else:
					ack['success'] = False
					ack['remark'] = "No such records"

			except Exception as e:
				print e

			cursor.close()
			cnx.close()

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"

	# return render_template("index.html", msg="welcome")


@app.route("/get_report", methods=['GET', 'POST'])
def get_report():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		print 'here', request.data
		if request.is_json:
			print "Json"
			content = request.get_json()
			print content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for getting reports :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)

			query = ("select dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp, login.aadhaar_no, name, authority_level from dam_data join dam join login on dam_data.dam_id = dam.dam_id and dam_data.aadhaar_no = login.aadhaar_no where time_stamp BETWEEN %(start_date)s AND %(end_date)s ")

			# The records can be ordered or grouped by certain column (e.g. dam_name or state) in above query if required

			# As of now, 'criteria' for report (state, priority, facility) is not taken into account

			try:
				cursor.execute(query, content)
				rows_affected = cursor.rowcount

				if rows_affected > 0:
					# Send user details :-
					#rows = cursor.fetch_all()
					#row = rows[0]

					ack['report'] = []

					for (dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp, aadhaar_no, name, authority_level) in cursor:
						repo = {}
						repo['dam_name'] = dam_name
						repo['nearest_city'] = nearest_city
						repo['state'] = state
						repo['river'] = river
						repo['latitude'] = latitude
						repo['longitude'] = longitude
						repo['seepage'] = seepage
						repo['cracks'] = cracks
						repo['erosion'] = erosion
						repo['gates_condition'] = gates_condition
						repo['sluice_gates_condition'] = sluice_gates_condition
						repo['max_flood_handled'] = max_flood_handled
						repo['energy_dissipator_condition'] = energy_dissipator_condition
						repo['instrument_condition'] = instrument_condition
						repo['descrip'] = descrip
						repo['time_stamp'] = str(time_stamp)
						repo['aadhaar_no'] = aadhaar_no
						repo['name'] = name
						repo['authority_level'] = authority_level

						ack['report'].append(repo)

					# indicate that the request was a success
					ack["success"] = True

				else:
					# indicate that the login request failed
					ack["success"] = False
					ack["remark"] = "No such records within the dates"

		 	except Exception as e:
		 		print e

			cursor.close()
			cnx.close()

			#ack.headers.add('Access-Control-Allow-Origin', '*')

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"

	#return render_template("index.html", msg="welcome")


@app.route("/get_my_records", methods=["POST"])
def get_my_records():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if flask.request.method == "POST":
		#print request.data
		if flask.request.is_json:
			content = flask.request.get_json()
			print content

			#print 'IP of sender : ', flask.request.remote_addr
			#print flask.request.environ['REMOTE_ADDR']

			# Code for getting records :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)

			query = ("select dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp from dam_data join dam on dam_data.dam_id = dam.dam_id where aadhaar_no = %(aadhaar_no)s AND time_stamp BETWEEN %(start_date)s AND %(end_date)s")

			try:
				cursor.execute(query, content)
				rows_affected = cursor.rowcount

				if rows_affected > 0:
					# Send user details :-
					ack['records'] = []

					print 'here'

					for (dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp) in cursor:
						rec = {}
						rec['dam_name'] = dam_name
						rec['nearest_city'] = nearest_city
						rec['state'] = state
						rec['river'] = river
						rec['latitude'] = latitude
						rec['longitude'] = longitude
						rec['seepage'] = seepage
						rec['cracks'] = cracks
						rec['erosion'] = erosion
						rec['gates_condition'] = gates_condition
						rec['sluice_gates_condition'] = sluice_gates_condition
						rec['max_flood_handled'] = max_flood_handled
						rec['energy_dissipator_condition'] = energy_dissipator_condition
						rec['instrument_condition'] = instrument_condition
						rec['descrip'] = descrip
						rec['time_stamp'] = str(time_stamp)

						ack['records'].append(rec)

					# indicate that the request was a success
					ack["success"] = True

				else:
					print "Here empty"
					ack["success"] = False
					ack["remark"] = "Empty"

			except Exception as e:
		 		print e

			# indicate that the request was a success
			ack["success"] = True
			
			print ack			
			
			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"
	#return render_template("index.html", msg="welcome") 
	

@app.route("/get_entry_details", methods=['GET', 'POST'])
def get_entry_details():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		print 'here', request.data
		if request.is_json:
			print "Json"
			content = request.get_json()
			print content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for getting reports :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)

			query = ("select dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp, login.aadhaar_no, name, authority_level from dam_data join dam join login on dam_data.dam_id = dam.dam_id and dam_data.aadhaar_no = login.aadhaar_no where time_stamp = %(time_stamp)s AND login.aadhaar_no = %(aadhaar_no)s AND dam_name = %(dam_name)s ")

			# The records can be ordered or grouped by certain column (e.g. dam_name or state) in above query if required
<<<<<<< HEAD

			# As of now, 'criteria' for report (state, priority, facility) is not taken into account

=======
		
>>>>>>> 492e490d7be0a1a68679f03ab1ffabf4723dbc1e
			try:
				cursor.execute(query, content)
				rows_affected = cursor.rowcount

				if rows_affected > 0:
					# Send user details :-
					#rows = cursor.fetch_all()
					#row = rows[0]

					ack['report'] = []

					for (dam_name, nearest_city, state, river, latitude, longitude, seepage, cracks, erosion, gates_condition, sluice_gates_condition, max_flood_handled, energy_dissipator_condition, instrument_condition, descrip, time_stamp, aadhaar_no, name, authority_level) in cursor:
						repo = {}
						repo['dam_name'] = dam_name
						repo['nearest_city'] = nearest_city
						repo['state'] = state
						repo['river'] = river
						repo['latitude'] = latitude
						repo['longitude'] = longitude
						repo['seepage'] = seepage
						repo['cracks'] = cracks
						repo['erosion'] = erosion
						repo['gates_condition'] = gates_condition
						repo['sluice_gates_condition'] = sluice_gates_condition
						repo['max_flood_handled'] = max_flood_handled
						repo['energy_dissipator_condition'] = energy_dissipator_condition
						repo['instrument_condition'] = instrument_condition
						repo['descrip'] = descrip
						repo['time_stamp'] = time_stamp
						repo['aadhaar_no'] = aadhaar_no
						repo['name'] = name
						repo['authority_level'] = authority_level

						ack['report'].append(repo)

					# indicate that the request was a success
					ack["success"] = True

				else:
					# indicate that the login request failed
					ack["success"] = False
					ack["remark"] = "No such records within the dates"

		 	except Exception as e:
		 		print e

			cursor.close()
			cnx.close()

			#ack.headers.add('Access-Control-Allow-Origin', '*')

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"

	#return render_template("index.html", msg="welcome")


@app.route("/save_entry_severity", methods=['GET', 'POST'])
def save_entry_severity():
	# initialize the ack dictionary that will be returned from the view
	ack = {"success": False}

	if request.method == "POST": #from android
		print 'here', request.data
		if request.is_json:
			print "Json"
			content = request.get_json()
			print content

			#print 'IP of sender : ', request.remote_addr
			#print request.environ['REMOTE_ADDR']

			# Code for getting reports :-
			cnx = mysql.connector.connect(user=username, password=dbpassword, host=host, database=database_name)
			cursor = cnx.cursor(buffered = True)
<<<<<<< HEAD

			query = ("UPDATE dam_data SET severity = (%(severity)s)  WHERE aadhaar_no = %(aadhaar_no)s AND time_stamp = %(time_stamp)s AND dam_id = (SELECT dam_id from dam where dam_name = %(dam_name)s ) " )

			try:
				cursor.execute(query, content)

				# Make sure data is committed to the database
				cnx.commit()

				message = "Please evacuate your premises, as the Dam in your locality is in a critical condition"
				username = "7972111755"
				passwd = "cajinkya21"

				message = "+".join(message.split(' '))

				url = 'http://site24.way2sms.com/Login1.action?'
				data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

				cj = cookiekib.CookieJar()
				opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

				opener.addheaders=[('User-Agent', 'Mozilla/5.0 (X-11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
				try:
					usock = opener.open(url, data)
				except IOError:
					print "error"

				jession_id = str(cj).split('~')[1].split(' ')[0]
				send_sms_url = 'http://site24.way2sms.com/smstoss.action?'


				for (mobile_no, ) in cursor:
					mobno = mobile_no
					# print "dam_id = ", damid

					send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+mobno+'&message='+message+'&msgLen=136'
					time.sleep(2)

				opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]

				try:
					sms_sent_page = opener.open(send_sms_url, send_sms_data)
				except IOError:
					print "Error"


				# indicate that the request was a success
				ack["success"] = True

=======
		
			query = ("UPDATE dam_data SET severity = (%(severity)s), time_stamp = time_stamp  WHERE aadhaar_no = %(aadhaar_no)s AND time_stamp = %(time_stamp)s AND dam_id = (SELECT dam_id from dam where dam_name = %(dam_name)s ) " )
			
			try:
				cursor.execute(query, content)
				rows_affected = cursor.rowcount
				print rows_affected

				if rows_affected == 1:
					# Make sure data is committed to the database
					cnx.commit()
			
					# indicate that the request was a success
					ack["success"] = True
					
				else:
					# indicate that the login request failed
					ack["success"] = False
					ack["remark"] = "No such record"
								
>>>>>>> 492e490d7be0a1a68679f03ab1ffabf4723dbc1e
		 	except Exception as e:
		 		print e

			if content['severity'] == "2":

				message = "Please evacuate your premises, as the Dam in your locality is in a critical condition"
				username = "7972111755"
				passwd = "cajinkya21"

				message = "+".join(message.split(' '))

				url = 'http://site24.way2sms.com/Login1.action?'
				data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

				cj = cookiekib.CookieJar()
				opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

				opener.addheaders=[('User-Agent', 'Mozilla/5.0 (X-11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
				try:
					usock = opener.open(url, data)
				except IOError:
					print "error"

				jession_id = str(cj).split('~')[1].split(' ')[0]
				send_sms_url = 'http://site24.way2sms.com/smstoss.action?'

				query = ("SELECT mobile_no FROM login WHERE city = (SELECT nearest_city FROM dam WHERE dam_name = %(dam_name)s)")

				try:
					cursor.execute(query, content)
					#cnx.commit()

					for (mobile_no, ) in cursor:
						mobno = mobile_no
						# print "dam_id = ", damid

						send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+mobno+'&message='+message+'&msgLen=136'
						time.sleep(2)

					ack["smssuccess"] = True
				except Exception as e:
					print e

				opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]

				try:
					sms_sent_page = opener.open(send_sms_url, send_sms_data)
				except IOError:
					print "Error"



			cursor.close()
			cnx.close()

			#ack.headers.add('Access-Control-Allow-Origin', '*')

			return flask.jsonify(ack)

		else:
			print "Not json"

	else:
		print "Not a POST request"

	#return render_template("index.html", msg="welcome")


if __name__ == '__main__':
	app.debug = True # shows the error log

	app.run(host='0.0.0.0') # this makes the web application accessible to any system over this network (useful for instant and parallal testing)
