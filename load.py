import couchdb
import json
import time
import csv

#READ THESE FROM CONFIG

db_full_url= ""
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
with open('hopcoms_daily_ratelist_2012.csv', "r") as csv_file:
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
				try:
					if hopcoms_daily[_id]:
						print "exists"
						data = hopcoms_daily[_id]						
				except couchdb.http.ResourceNotFound:
						print "add"
						data = {}
						data["_id"]=_id

				if item_code:
					if column != '' and column != 'NR':
						data[item_code]=float(column)
					else:
						data[item_code]=None
					print str(data)
					hopcoms_daily.save(data)
			column_no = column_no + 1			