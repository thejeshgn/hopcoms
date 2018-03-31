import couchdb
import json
import time
import csv

#READ THESE FROM CONFIG
config_file = "/home/thej/.config/code_config/hopcoms.json"
config  = json.load(open(config_file))
db_full_url= config["db_full_url"]

couch = couchdb.Server(db_full_url)
hopcoms_daily 	= couch["hopcoms_daily"]
all_item_list = {}

with open('item_list.csv', "r") as csv_file:
	reader = csv.reader(csv_file)
	header = True
	for row in reader:
		if header:
			header = False
			continue
		all_item_list[(row[1]).strip()]=int(row[0])

#print str(all_item_list)


column_headers = []
with open('hopcoms_daily_ratelist_2017.csv', "r") as csv_file:
	all_documents = {}
	reader = csv.reader(csv_file)
	header = True
	for row in reader:
		if header:
			header = False
			column_headers = row
			print str(column_headers)
			continue
		data = {}
		item_code = None
		column_no = 0
		for column in row:
			print column_no
			if column_no == 0:
				data = {}				
				item_code = None
			if column_no == 1:
				item_name = column.strip()
				if item_name == '':
					break
				item_code = all_item_list[item_name]
				
			if column_no > 1:
				given_date = column_headers[column_no]
				_id = ''.join(reversed(given_date.split("/")))
				print str(_id)
				if all_documents.has_key(_id):
					data = all_documents[_id]
				else:
					data = {}
					data["_id"]=_id

				if item_code:
					if column != '' and column != 'NR' and float(column) != 0:
						data[item_code]=float(column)
						
				all_documents[_id] = data

			column_no = column_no + 1			
	#all rows are over
	data = None
	for key, data in all_documents.iteritems():
		print "============================================================================================"
		_id = data["_id"]
		try:
			if hopcoms_daily[_id]:
				print "exists"
				x = hopcoms_daily[_id]
				print str(x["_id"])
				print str(x["_rev"])
				data["_rev"] = x["_rev"]						
		except couchdb.http.ResourceNotFound:
				print "add"
				data["_id"]=_id

		print str(data)
		hopcoms_daily.save(data)
